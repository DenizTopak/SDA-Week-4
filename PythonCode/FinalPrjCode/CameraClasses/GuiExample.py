import cv2
from GUI import *


        
video = cv2.VideoCapture(0)



x1, y1, x2, y2 = 115, 135, 385, 475

Ui = GUI(x1, x2, y1, y2)

if (video.isOpened() == False):
    print('Error opening stream')

#start the stream
while(video.isOpened()):
    ret, frame = video.read()
    cropped_frame = frame[y1:y2, x1:x2]
    


    if ret == True:
        Ui.DrawLabelTop(cropped_frame, named_colors["black"])
        Ui.Text(cropped_frame, 'Triangle: Red - Coordinates (X, Y)', (0, line[0]), named_colors['white'])
        Ui.Text(cropped_frame, 'Triangle: Red - Coordinates (X, Y)', (0, line[1]), named_colors['white'])
        Ui.Text(cropped_frame, 'Triangle: Red - Coordinates (X, Y)', (0, line[2]), named_colors['white'])
        cv2.imshow('Window', cropped_frame)
        
        k = cv2.waitKey(20)
        if k == ord('q'):
             break
    else:
        break

video.release()
cv2.destroyAllWindows()




