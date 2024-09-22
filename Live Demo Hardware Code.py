#--------------------------------------------------------------------------------
import sys
sys.path.append('../')
from Common.hardware_project_library import *

hardware = True
QLabs = configure_environment(project_identifier, ip_address, hardware).QLabs
if project_identifier == 'P3A':
    arm = qarm(project_identifier,ip_address,QLabs,hardware)
    table = servo_table(ip_address,QLabs,None,hardware)
else:
    speed = 0.1 # in m/s
    bot = qbot(speed,ip_address,QLabs,project_identifier,hardware)
#--------------------------------------------------------------------------------
#CODE BEGINS
#---------------------------------------------------------------------------------
#declaring bot_full variable
bot_full = True

def transfer_container(bot_full):

    #activates line following, colour and ultrasonic sensors
    bot.activate_line_following_sensor()
    bot.activate_color_sensor()
    bot.activate_stepper_motor()
    dumped = False
    while bot_full == True:
        try:
            color_sensor_output = bot.read_color_sensor()
            print(color_sensor_output)

            #drops off container(s) at red bin
            if color_sensor_output[1][0]>120 and dumped == False:
                print("found red")
            
                #bot stops in front of bin and drops off container into bin
                bot.stop()
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                dumped = True

            #drops off container(s) at green bin
            if color_sensor_output[1][1]>120 and dumped == False:
                print("found green")
                bot.stop()
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                dumped = True

            #drops off container(s) at blue bin
            if color_sensor_output[1][2]>120 and dumped == False:
                print("found blue")
                bot.stop()
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                bot.linear_actuator_out(3)
                time.sleep(2)
                dumped = True
                
            #bot continues to move again
            line_sensor_output = bot.line_following_sensors()
            print(line_sensor_output)

            #checks if bot is moving straight
            if line_sensor_output[0] == 1 and line_sensor_output[1] == 1:
                # sets bot wheel speed
                bot.set_wheel_speed([0.08,0.08])

            elif line_sensor_output[1] == 0:
                # sets bot wheel speed
                bot.set_wheel_speed([0.03,0.08])

            elif line_sensor_output[0] == 0:
                # sets bot wheel speed
                bot.set_wheel_speed([0.08,0.03])

        except:
            time.sleep(0.1)
            continue