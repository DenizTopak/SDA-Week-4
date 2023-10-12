import sys
import DoBot as Dbt             # add DoBot class code
from CameraClasses import Camera as Cm  # add camera and UI class code
import time
from serial.tools import list_ports


x1, y1, x2, y2 = 115, 135, 385, 475


def main():

    
    port = port_selection()
    homeX, homeY, homeZ = 200, 0, 50
    topLeftX, topLeftY = 0, 0
    bottomRightX, bottomRightY = 0, 0
    groundLVL = 0
    
    print("Connecting")
    
    print("initialising DoBot")
    botController = Dbt.DoBotArm(port, homeX, homeY, homeZ)
    print("initialising Camera")
    camera = Cm.Camera(None, x1, y1, x2, y2)

    time.sleep(5)
    print("initialising Complete")

    input('To calibrate arm to the vision field, move the arm suction cup to the top-left corner of the camera vision field, touching the floor, followed by [Enter]')
    topLeftX, topLeftY, groundLVL = botController.getPosition()[0], botController.getPosition()[1], botController.getPosition()[2] 
    print(topLeftX, topLeftY, groundLVL)

    input('Now move the arm suction cup to the bottom-right corner of the camera vision field, followed by [Enter]')
    bottomRightX, bottomRightY = botController.getPosition()[0], botController.getPosition()[1] 
    print(bottomRightX, bottomRightY)
    
    time.sleep(2)

    botController.moveArmXYZ(topLeftX, topLeftY + 60, groundLVL + 50)

    time.sleep(2)

    print("done callibrating, starting arm functionality")

    while True:
        camera.doCameraThings()
        if (camera.selected_shape_info != None):
            print(botController.getPosition())
        # botController.moveArmXY()
    

def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device


# run the main method
if (__name__ == '__main__'):
    main()