import cv2
from pygame.locals import *

class Camera():

    # Init camera object
    def __init__(self, selected_shape_info, x1, y1, x2, y2):
        # Constants for cropping camera view
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2

        # Information about clicked shape coordinates
        self.selected_shape_infoX = selected_shape_info
        self.selected_shape_infoY = selected_shape_info

        # Create a VideoCapture object for the camera (camera index 0 for built-in camera)
        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)   

        # Check if the camera was opened successfully
        if not self.cap.isOpened():
            print("Error: Could not open the camera.")
            exit()

        cv2.namedWindow("DoBot camera control")
        cv2.setMouseCallback("DoBot camera control", self.on_mouse)
        

    # Function to detect and identify objects in the frame
    def detect_objects(self, frame, x1, y1, x2, y2):
        # Crop the frame using the specified coordinates
        cropped_frame = frame[y1:y2, x1:x2]

        # Rotate image to match dobot and camera axis 
        trueFrame = cv2.rotate(cropped_frame, cv2.ROTATE_90_CLOCKWISE)

        # Convert the cropped frame to grayscale
        gray = cv2.cvtColor(trueFrame, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Detect edges using Canny edge detector
        edges = cv2.Canny(blurred, 50, 150)

        # Find contours in the edge map
        contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        # List to store center points and shape
        self.center_points = []

        # Iterate through detected contours
        for contour in contours:
            # filter out small contours
            if cv2.arcLength(contour, True) > 50:
                # Approximate the contour to determine its shape
                epsilon = 0.04 * cv2.arcLength(contour, True)
                approx = cv2.approxPolyDP(contour, epsilon, True)

                # Get the centroid of the contour
                M = cv2.moments(contour)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])

                    # Determine the color at the centroid
                    color = trueFrame[cy, cx]
                    color_name = ""
                    if color[1] > 100 and color[2] < 100 and color[0] < 200:  # Green
                        color_name = "Green"
                    elif color[2] > 180 and color[1] > 180:  # Yellow
                        color_name = "Yellow"
                    elif color[0] > 200:  # Blue
                        color_name = "Blue"
                    else:
                        color_name = "Red"

                    # Identify the shape based on the number of sides
                    if len(approx) == 3:
                        shape = "Triangle"
                    elif len(approx) == 4:
                        shape = "Square"
                    else:
                        shape = "Circle"

                    object_info = f"{shape}: {color_name} - Coordinates: ({cx}, {cy})"
                    self.center_points.append((cx, cy, shape, color_name, object_info))

                    # Draw the shape and color text on the cropped frame
                    text_color = (255, 255, 255)
                    cv2.putText(trueFrame, object_info, (cx - 50, cy - 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, text_color, 2)

                    # Draw a contour around the detected shape on the cropped frame
                    cv2.drawContours(trueFrame, [approx], -1, (0, 255, 0), 2)

                    # Draw a circle at the centroid on the cropped frame
                    cv2.circle(trueFrame, (cx, cy), 5, (0, 0, 255), -1)

        return trueFrame, self.center_points


    # Define a callback function for mouse events
    def on_mouse(self, event, x, y, flags, param):
        self.selected_shape_infoX = None
        self.selected_shape_infoY = None
        if event == cv2.EVENT_LBUTTONDOWN:
            for i, (cx, cy, shape, color_name, object_info) in enumerate(self.center_points):
                if abs(x - cx) < 10 and abs(y - cy) < 10:
                    self.selected_shape_infoX = cx
                    self.selected_shape_infoY = cy
                    print(f"Selected Object {i + 1}: {object_info}")
                    
    

    def doCameraThings(self):
        # Read a frame from the camera
        ret, frame = self.cap.read()

        # Detect and identify objects in the frame and crop it
        cropped_frame, center_points = self.detect_objects(frame, self.x1, self.y1, self.x2, self.y2)        

        # Display the cropped frame with detected objects and their colors
        cv2.imshow('Object Detection', cropped_frame)

        # Check for a key press to exit the loop (press 'q' key)
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            self.quitCamera()
            exit()

    def quitCamera(self):
        # Release the VideoCapture object and close any OpenCV windows
        self.cap.release()
        cv2.destroyAllWindows()