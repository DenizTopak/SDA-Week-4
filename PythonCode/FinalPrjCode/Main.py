import sys
import DoBot as Dbt             # add DoBot class code
from CameraClasses import Camera as Cm  # add camera and UI class code
import time
from serial.tools import list_ports

# Constants for camera frame cropping
x1, y1, x2, y2 = 115, 135, 385, 475

# Scale factors for matching camera coordinates to DoBot coordinates
xScaleFactor = 2.08
yScaleFactor = 2.12
yAddFactor = 20
xAddFactor = -4


def main():
    
    port = port_selection()
    homeX, homeY, homeZ = 70, -200, 60
    topLeftX, topLeftY = 0, 0
    groundLVL = 0
    
    # Create and init objects
    print("initialising DoBot")
    botController = Dbt.DoBotArm(port, homeX, homeY, homeZ) 
    print("initialising Camera")
    camera = Cm.Camera(None, x1, y1, x2, y2)

    # Sleep 10s to account for DoBot homing routine
    time.sleep(10)
    print("initialising Complete")

    # Get some coordinates to determine the real world position of the arm and conveyor belt, this should make the code more flexible
    input('To calibrate arm to the vision field, move the arm suction cup to the far-left corner of the camera vision field compared to the arm, touching the floor, followed by [Enter]')
    topLeftX, topLeftY, groundLVL = botController.getPosition()[0], botController.getPosition()[1], botController.getPosition()[2] 
    print(topLeftX, topLeftY, groundLVL)

    input('Now move the arm suction cup to the desired conveyor drop zone touching the belt, followed by [Enter]')
    conveyorX, conveyorY, conveyorHeight = botController.getPosition()[0], botController.getPosition()[1], botController.getPosition()[2] 
    print(conveyorX, conveyorY, conveyorHeight)


    # move to home pos
    time.sleep(2)
    botController.moveArmXYZ(homeX, homeY, homeZ)
    time.sleep(3)

    # Instructions for user
    print("Done callibrating, starting arm functionality")
    print("Click a shape centroid have the arm move it, press q to quit")

    while True:
        # Run vision code
        camera.doCameraThings()
        
        # if a shape is clicked in the UI
        if (camera.selected_shape_infoX != None and camera.selected_shape_infoY != None):
            
            # Ask user for command
            response1 = input("press [q] to exit, [g] to grab clicked shape, [s] to manually toggle suction if in wrong state, [h] to rehome (followed by [Enter])")
            # Quit program (also works when q is pressed in the UI window)
            if(response1 == "q"):
                break
            # Grab and move the clicked object
            elif(response1 == "g"):
                # Print target coordinate
                print("moving to x y")
                print(camera.selected_shape_infoX)
                print(camera.selected_shape_infoY)
                cX = camera.selected_shape_infoX
                cY = camera.selected_shape_infoY 
                grabObj(botController, cX, cY, topLeftX, topLeftY, groundLVL, conveyorX, conveyorY, conveyorHeight)
            # Manually toggle the suction state in case it is still on from a previous run
            elif(response1 == "s"):
                botController.toggleSuction()
            # Manually home the arm in case something went wrong and it is not in a good position
            elif(response1 == "h"):
                botController.moveHome()
            
            else:
                print("unknown command") 
                

# Function for port selection, generally not needed but used in case of multiple usb devices
def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device

# Picking sequence function, including translation of camera coordinates to DoBot coordinates
def grabObj(botController, cX, cY, topLeftX, topLeftY, groundLVL, conveyorX, conveyorY, conveyorHeight):

    # Calculate target DoBot coordinates using current object pixel coordinates
    targetX = topLeftX - (cX / xScaleFactor) + xAddFactor
    targetY = topLeftY + (cY / yScaleFactor) + yAddFactor

    # Move to safe position in case this has not been done aleady
    botController.moveHome()

    # Move above object to be picked
    botController.moveArmXYZ(targetX, targetY, groundLVL + 30)
    time.sleep(1)

    # Grab the object
    botController.toggleSuction()
    botController.moveArmXYZ(targetX, targetY, groundLVL+15)
    time.sleep(1)
    botController.moveArmXYZ(targetX, targetY, groundLVL+50)

    # Move arm to safe position to avoid locking the arm
    botController.moveHome()
    
    # Drop object on the conveyor belt
    botController.moveArmXYZ(conveyorX, conveyorY, conveyorHeight+35)
    time.sleep(1)
    botController.toggleSuction()
    time.sleep(1)
    botController.moveArmXYZ(conveyorX, conveyorY, conveyorHeight+50)

    # Move to safe position
    botController.moveHome()

    # Move conveyor belt
    botController.SetConveyor(True, -15000)
    time.sleep(2)
    botController.SetConveyor(False)
    

# run the main method
if (__name__ == '__main__'):
    main()

