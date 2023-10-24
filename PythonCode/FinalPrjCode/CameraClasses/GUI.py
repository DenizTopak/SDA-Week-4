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
    def __init__(self, window, x1, x2, y1, y2):
        self.window = window
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def DrawLabelTop(self, bg_color):
        thickness = cv2.FILLED

        cv2.rectangle(self.window, (0, 0), (300, 50), bg_color, thickness)
    
    def Text(self, text, pos, bg_color):
        font_face = cv2.FONT_HERSHEY_SIMPLEX
        scale = 0.4
        color = bg_color
        
        cv2.putText(self.window, text, pos, font_face, scale, color, 1, cv2.LINE_AA)
