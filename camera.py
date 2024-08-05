import cv2 as cv

class Camera:
    def __init__(self, index=0):
        self.camera = cv.VideoCapture(index)
        if not self.camera.isOpened():
            raise ValueError(f"Unable to open camera with index {index} :(")
        
        self.width = self.camera(cv.CAP_PROP_FRAME_WIDTH)
        self.height = self.camera(cv.CAP_PROP_FRAME_HEIGHT)
        
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
