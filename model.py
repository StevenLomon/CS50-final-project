# Linear support classifier gives decent results and doesn't need too long to train
# For production purposes a CNN would give much higher quality predictions
import PIL.Image
from sklearn.svm import LinearSVC
import numpy as np
import cv2 as cv
import PIL

class Model:
    def __init__(self):
        self.model = LinearSVC()
    
    # Process the images by turning the images into numpy arrays that can be used by the model
    def train_model(self, counter):
        img_list = np.array([])

        for i in range(1, counter):
            img = cv.imread(f"ducks/frame{i}.jpg")[:,:,0] # Everything, everything, first dimension
            img = img.reshape(16000) # 150 * 112
            img_list = np.append(img_list, [img])
        
        img_list = img_list.reshape(counter - 1, 16800)
        self.model.fit(img_list) #class_list??
        print("Model succesfully trained!")

    def predict(self, frame):
        frame = frame[1] # The argument frame is a tuple where the actual frame is the second element
        cv.imwrite('frame.jpg', cv.cvtColor(cv.COLOR_BGR2RGB))
        img = PIL.Image.open('frame.jpg')
        img.thumbnail(150,150), PIL.Image.ANTIALIAS
        img.save('frame.jpg')

        img = cv.imread('frame.jpg')[:,:,0]
        img = img.reshape(16800)

        prediction = self.model.predict([img])

        return prediction[0]
