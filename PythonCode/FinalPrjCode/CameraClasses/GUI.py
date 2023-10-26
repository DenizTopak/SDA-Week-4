import cv2

#Define colors as dictionary
named_colors = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "yellow": (255, 255, 0),
    "magenta": (255, 0, 255),
    "cyan": (0, 255, 255),
    "white": (255, 255, 255),
    "black": (0, 0, 0)
}

line = [10, 25, 40]

class GUI():
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def DrawLabelTop(self,window, bg_color):
        thickness = cv2.FILLED

        cv2.rectangle(window, (0, 0), (300, 50), bg_color, thickness)
    
    def Text(self, window, text, pos, bg_color):
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        color = bg_color
        
        cv2.putText(window, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
    
    named_colors = {
        "red": (255, 0, 0),
        "green": (0, 255, 0),
        "blue": (0, 0, 255),
        "yellow": (255, 255, 0),
        "magenta": (255, 0, 255),
        "cyan": (0, 255, 255),
        "white": (255, 255, 255),
        "black": (0, 0, 0)
    }

    line = [10, 25, 40]

        
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




