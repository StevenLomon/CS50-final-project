import cv2 as cv

class Camera:
    def __init__(self):
        self.camera = cv.VideoCapture(0) # 0 specifies the first webcam available on the computer
        if not self.camera.isOpened(): # If there is an error of any sorts
            raise ValueError("Unable to open camera :(")
        
    def __del__(self): # Close camera when application is closed
        if self.camera.isOpened():
            self.camera.release()
    
    def get_frame(self): # Method for getting the next frame from a camera instance
        if self.camera.isOpened():
            ret, frame = self.camera.read()

            if ret:
                # Processed images in OpenCV are returned as BGR. We want to convert this to RGB instead
                return (ret, cv.cvtColor(frame, cv.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return None
