import os
import tkinter as tk
from tkinter import simpledialog
import cv2 as cv
import PIL.Image, PIL.ImageTk
import camera

class App:
    def __init__(self, window=tk.Tk(), window_title="Duck Classifier"):
        self.window = window
        self.window_title = window_title

        # An array to keep track of the name of the class followed by a number
        # self.counters = [1, 1]

        # self.model = 

        self.auto_predict = False

        self.camera = camera.Camera()
        self.init.gui()

        self.delay = 15
        # self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()

    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.camera.width, height=self.camera.height)
        self.canvas.pack()

        self.btn_toggleauto = tk.Button(self.window, text="Auto Prediction", width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

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