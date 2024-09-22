import random

#storing mass of bin and total mass variables
mass = 0
total_mass = 0
count = 0

#storing bin number variables
bin_number = 1
bin_current = 0
bin_last = 0

#setting initial servotable variable
servotable_full = False

#dispense container
def dispense_container():
   
    global total_mass
    global bin_current
    bottle_properties = table.dispense_container(random.randint(1,6),True)
    print(bottle_properties)
    bin_current = bottle_properties[2]
    total_mass += bottle_properties[1]

#defining a function to load container with q arm
def pickup_container():

    #grips container from home position
    arm.home()
    arm.rotate_elbow(-35)
    arm.rotate_shoulder(49)
    arm.control_gripper(33)
    time.sleep(1.3)
   
    #takes container out of servotable
    arm.rotate_shoulder(-49)
    arm.rotate_elbow(35)
    arm.rotate_base(-95)
   
#defining a function to transfer container to hopper
def dropoff_container(count):
   
    #drops off container at a specific position in hopper based on container number
    arm.move_arm(0.005, -0.48, 0.528)
    arm.rotate_shoulder(3)
       
    #releases container and returns home
    time.sleep(1)
    arm.control_gripper(-33)
    time.sleep(1)
    arm.rotate_shoulder(-45)
    time.sleep(1)
    arm.home()
   
#create a conditional loop (can repeat for a max of 3 times)
def dispense_cycle():
    global total_mass
    global bin_number
    global bin_current
    global bin_last
    global servotable_full

    #resets count and total mass for every cycle
    count = 0
    total_mass = 0

    #the q bot will only pick up a new container if it meets the criteria
    #total mass must be less than 90, bin number must be same, 3 containers max
    while count < 3 and total_mass < 90:

        if servotable_full == False:
            dispense_container()

        #qbot doesn't pick up new container if total mass is greater than 90
        if total_mass >= 90:
            servotable_full = True
            break
           
        else:

            # checks if there is an existing container on servotable
            # checks if new container is going to same location as previous container
            if servotable_full == True or bin_current == bin_last or bin_last == 0:

                pickup_container()
                dropoff_container(count)  
                time.sleep(1.3)

                # only a maximum of 3 containers can be placed on a hopper
                count += 1
                servotable_full = False

                if count < 3:
                    bin_last = bin_current

            # loop terminates if new container is not going to same location
            else:
                servotable_full = True
                break
           
                #prevents arm from interfering with bottles
                arm.home()

        bot_full = True

def transfer_container(bot_full):
   
    #converts the assigned bin into an integer
    global bin_last
    bin_number = int(bin_last.strip("Bin0"))
   
    print(bin_number)

    #activates line following, colour and ultrasonic sensors
    bot.activate_line_following_sensor()
    bot.activate_color_sensor()
    bot.activate_ultrasonic_sensor()

    while bot_full == True:
   
        color_sensor_output = bot.read_color_sensor()
        print(color_sensor_output)
        US_sensor_output = bot.read_ultrasonic_sensor()
        print(US_sensor_output)
               
        #drops off container(s) at bin 1
        if bin_number == 1 and US_sensor_output < 0.5 and color_sensor_output[0][0] == 1:

                #positions qbot in front of bin
                bot.stop()
                bot.forward_distance(0.2)
                bot.rotate(-25)
                bot.forward_distance(0.12)

                #tilts/empties hopper to drop off container(s)
                bot_full = False
                return bot_full
           
        #drops off container(s) at bin 2
        elif bin_number == 2 and US_sensor_output < 0.5 and color_sensor_output[0][1] == 1:

                bot.stop()
                bot.rotate(-10)
                bot.forward_distance(0.15)

                bot_full = False
                return bot_full

        #drops off container(s) at bin 3
        elif bin_number == 3 and US_sensor_output < 0.5 and color_sensor_output[0][0] == 0 and color_sensor_output[0][2] == 1:

                bot.stop()
                bot.forward_distance(0.15)
                bot.rotate(-15)
                bot.forward_distance(0.25)

                bot_full = False
                return bot_full
                bot.rotate(10)

        #drops off container(s) at bin 4
        elif bin_number == 4 and US_sensor_output < 0.5 and color_sensor_output[0][0] == 1 and color_sensor_output[0][2] == 1:

                bot.stop()
                bot.rotate(-10)
                bot.forward_distance(0.2)


                bot_full = False
                return bot_full

        line_sensor_output = bot.line_following_sensors()
        print(line_sensor_output)
       
        #checks if bot is moving straight
        if line_sensor_output[0] and line_sensor_output[1] == 1:
           
            # sets bot wheel speed
            bot.set_wheel_speed([0.08,0.08])

        #bot's wheel speed for turning left
        elif line_sensor_output[1] == 0:
            bot.set_wheel_speed([0.03,0.08])

        #bot's wheel speed for turning right
        elif line_sensor_output[0] == 0:
            bot.set_wheel_speed([0.08,0.03])

       
               
    else:
        bot.stop()


def deposit_container():
    #position bot at coordinates in front of bin
    #rotate to face the proper direction for dumping mechanism

    #activates hopper to rotate
    bot.activate_linear_actuator()

    #rotates hopper in increments of 15 degrees for 6 loops
    for i in range(1,7):
        bot.rotate_hopper(i*15)
        time.sleep(0.3)

    #returns hopper to original position
    time.sleep(1.2)
    bot.rotate_hopper(0)

def return_home():

    bot.activate_line_following_sensor()

    bot_location = list(bot.position())

#checks if qbot is at home position
#while qbot is not at home position, it will continue to move
    while bot_location[0]<1.46 or(bot_location[1]<-0.012 or bot_location[1]>0.012):

        bot_location = bot.position()
       
        line_sensor_output = bot.line_following_sensors()

        if line_sensor_output[0] and line_sensor_output[1] == 1:
            bot.set_wheel_speed([0.08,0.08])

        elif line_sensor_output[1] == 0:
            bot.set_wheel_speed([0.03,0.08])

        elif line_sensor_output[0] == 0:
            bot.set_wheel_speed([0.08,0.03])

    #stops qbot at home position
    else:
        bot.stop()

        #mini adjustments to qbot's home position before next cycle
        bot.rotate(-7)
        bot.forward_distance(0.01)

#main function
def main():
    dispense_cycle()
    print(bin_current)
    transfer_container(True)
    deposit_container()
    return_home()

    #infinite recursive cycles
    main()