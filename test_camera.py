import cv2

def test_camera(index):
    cap = cv2.VideoCapture(index)
    if not cap.isOpened():
        print(f"Camera with index {index} cannot be opened.")
    else:
        print(f"Camera with index {index} is working.")
        cap.release()

# Test the default camera
test_camera(0)