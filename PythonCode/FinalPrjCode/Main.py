import sys
import DoBot as Dbt             # add DoBot class code
from CameraClasses import Camera as Cm  # add camera and UI class code
import time
from serial.tools import list_ports


x1, y1, x2, y2 = 115, 135, 385, 475

xScaleFactor = 2.08
yScaleFactor = 2.12 # 1.8, smaller for more inwards
yAddFactor = 20
xAddFactor = -4


def main():
    
    port = port_selection()
    homeX, homeY, homeZ = 70, -200, 60
    topLeftX, topLeftY = 0, 0
    groundLVL = 0
    
    print("Connecting")
    
    print("initialising DoBot")
    botController = Dbt.DoBotArm(port, homeX, homeY, homeZ) 
    print("initialising Camera")
    camera = Cm.Camera(None, x1, y1, x2, y2)

    time.sleep(10)
    print("initialising Complete")

    input('To calibrate arm to the vision field, move the arm suction cup to the far-left corner of the camera vision field, touching the floor, followed by [Enter]')
    topLeftX, topLeftY, groundLVL = botController.getPosition()[0], botController.getPosition()[1], botController.getPosition()[2] 
    print(topLeftX, topLeftY, groundLVL)

    input('Now move the arm suction cup to the desired conveyor drop zone touching the belt, followed by [Enter]')
    conveyorX, conveyorY, conveyorHeight = botController.getPosition()[0], botController.getPosition()[1], botController.getPosition()[2] 
    print(conveyorX, conveyorY, conveyorHeight)

    time.sleep(5)

    # move to home pos
    botController.moveArmXYZ(homeX, homeY, homeZ)
    time.sleep(3)

    print("done callibrating, starting arm functionality")

    while True:
        camera.doCameraThings()
        if (camera.selected_shape_infoX != None and camera.selected_shape_infoY != None):
            print(botController.getPosition())
            response1 = input("q to exit, g to grab shape, s to toggle suction if in wrong state, h for rehome")
            # response2 = input("Give y  (int), r for real run")
            # response3 = input("Give z  (int)")
            if(response1 == "q"):
                break
            elif(response1 == "g"):
                print("moving to x y")
                print(camera.selected_shape_infoX)
                print(camera.selected_shape_infoY)
                cX = camera.selected_shape_infoX
                cY = camera.selected_shape_infoY 
                grabObj(botController, cX, cY, topLeftX, topLeftY, groundLVL, conveyorX, conveyorY, conveyorHeight)
            elif(response1 == "s"):
                botController.toggleSuction()
            elif(response1 == "h"):
                botController.moveHome()

            else:
                print("unknown command") 
            # else:
            #     botController.moveArmXYZ(int(response1), int(response2), int(response3))
            #     time.sleep(2)
            #     print("moved to")
            #     print(botController.getPosition())
                
    time.sleep(5)

    

def port_selection():
    # Choosing port
    available_ports = list_ports.comports()
    print('Available COM-ports:')
    for i, port in enumerate(available_ports):
        print(f"  {i}: {port.description}")

    choice = int(input('Choose port by typing a number followed by [Enter]: '))
    return available_ports[choice].device


def grabObj(botController, cX, cY, topLeftX, topLeftY, groundLVL, conveyorX, conveyorY, conveyorHeight):
    # move to safe pos in case this hasnt been done aleady
    botController.moveHome()

    # move above
    botController.moveArmXYZ(topLeftX - (cX / xScaleFactor)+ xAddFactor, topLeftY + (cY / yScaleFactor) + yAddFactor, groundLVL+30)
    time.sleep(1)

    # grab
    botController.toggleSuction()
    botController.moveArmXYZ(topLeftX - (cX / xScaleFactor) + xAddFactor, topLeftY + (cY / yScaleFactor) + yAddFactor, groundLVL+15)
    time.sleep(1)
    botController.moveArmXYZ(topLeftX - (cX / xScaleFactor) + xAddFactor, topLeftY + (cY / yScaleFactor) + yAddFactor, groundLVL+50)

    # move to safe pos
    botController.moveHome()
    # time.sleep(1)
    
    # drop on belt
    botController.moveArmXYZ(conveyorX, conveyorY, conveyorHeight+35)
    time.sleep(1)
    botController.toggleSuction()
    time.sleep(1)
    botController.moveArmXYZ(conveyorX, conveyorY, conveyorHeight+50)

    # move to safe pos
    botController.moveHome()
    time.sleep(1)

    # move belt
    botController.SetConveyor(True, -15000)
    time.sleep(2)
    botController.SetConveyor(False)
    

# run the main method
if (__name__ == '__main__'):
    main()

