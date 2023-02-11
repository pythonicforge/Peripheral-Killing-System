import tkinter as tk

# Importing all external modules
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import ImageTk, Image
import screen_brightness_control as sbc


class GesturedBrightness:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Brightness Control Console")

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.5, maxHands=1)

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        ret, frame = self.cap.read()

        cv2.putText(frame, f"BRIGHTNESS: {int(sbc.get_brightness()[0])}%", (
            40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (2, 0, 63), 2)

        hands, frame = self.detector.findHands(frame, draw=True, flipType=True)
        if hands:

            if (len((hands[0]["lmList"])) != 0):
                fingers = self.detector.fingersUp(hands[0])

                if (fingers[0] == 1 and fingers[1] == 1):
                    length, _, frame = self.detector.findDistance(
                        hands[0]["lmList"][4], hands[0]["lmList"][8], frame)

                    brightness = np.interp(length, [10, 290], [0, 100])

                    sbc.set_brightness(brightness, force=True)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)