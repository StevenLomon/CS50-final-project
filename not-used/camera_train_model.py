import os
import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import PIL.Image, PIL.ImageTk
import camera, model

class App:
    def __init__(self, window=tk.Tk(), window_title="Duck Classifier"):
        self.window = window
        self.window_title = window_title

        # An int to keep track of the name of the file name
        self.counters = 1

        self.model = model.Model()

        self.auto_predict = False

        self.camera = camera.Camera()
        self.init.gui()

        self.delay = 15
        self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_save_frame = tk.Button(self.window, text="Save frame for training", width=50, command=lambda: self.save_frame)
        self.btn_save_frame.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text="Train Model", width=50, command=lambda: self.model.train_model(self.counters))
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text="Predcit", width=50, command=self.predict)
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text="Reset", width=50, command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)

        self.class_label = tk.Label(self.window, text="CLASS")
        self.class_label.config(font=("Arial", 20))
        self.class_label.pack(anchor=tk.CENTER, expand=True)

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict # Negating what it already is, chaning its current state

    def save_frame(self):
        ret, frame = self.camera.get_frame()
        if not os.path.exists('ducks'):
            os.mkdir('ducks')

        # We're gonna choose to write with color rather than grayscale since the yellow (default and the 
        # color of my duck) rather distinguishable feature of a rubber duck :))
        filename = f"ducks/frame{self.counter}.jpg"
        cv.imwrite(filename, cv.cvtColor(frame, cv.COLOR_BGR2RGB))

        # Resize for processing purposes
        img = PIL.Image.open(filename)
        img.thumbnail(150,150), PIL.Image.ANTIALIAS
        img.save(filename)

        # Increase the counter to continue keeping track of file names
        self.counter += 1

    def reset(self): # Delete training images and reset everything back to default values
        for file in os.listdir("ducks"):
            file_path = os.path.join("ducks", file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

        self.counter = 1
        self.model = model.Model()

    # For auto-predict
    def update(self):
        if self.auto_predict:
            self.predict()
        
        ret, frame = self.camera.get_frame()

        if ret:
            # Convert the frame from the camera to a Tk Image
            self.photo = PIL.ImageTk(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0,0, image=self.photo, anchor=tk.NW)

        # Recursively call the function over and over given a delay
        self.window(self.delay, self.update)

    def predict(self):
        frame = self.camera.get_frame()
        prediction = self.model.predict(frame)

        if prediction == 1:
            self.class_label.config(text="Duck")
            return "Duck"
        else:
            self.class_label.config(text="No duck")
            return "No duck"