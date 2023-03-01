import tkinter as tk
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import ImageTk, Image
import pyautogui


class AirMouse:
    def __init__(self):
        pyautogui.FAILSAFE = False

        self.window = tk.Tk()
        self.screen = (self.window.winfo_screenwidth(),
                       self.window.winfo_screenheight())

        self.window.title("Mouse Control Console")
        self.window.geometry("640x480")
        self.window.resizable(False, False)

        self.left, self.top, self.right, self.bottom = (90, 90, 550, 390)
        self.smoothening = 10
        self.previous_x, self.previous_y = 0, 0
        self.x_buffer, self.y_buffer = [0]*self.smoothening, [0]*self.smoothening

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.5, maxHands=1)

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def euclidean_distance(self, pt1, pt2):
        distance = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

        return distance

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)

        cv2.rectangle(frame, (self.left, self.top),
                      (self.right, self.bottom), (0, 0, 255), 2)

        hands, frame = self.detector.findHands(
            frame, draw=True, flipType=False)

        if hands is not None and len(hands) > 0:

            fingers = self.detector.fingersUp(hands[0])

            if (fingers[1] == 1 and fingers[2] == 0):

                handLms = hands[0]["indexCoords"]

                if handLms is not None:
                    cv2.circle(frame, (handLms[0], handLms[1]),
                               15, (0, 0, 255), cv2.FILLED)

                    index_X = np.interp(
                        handLms[0], (90, 640-90), (0, self.screen[0]))
                    index_Y = np.interp(
                        handLms[1], (90, 480-90), (0, self.screen[1]))
                    
                    self.x_buffer.pop(0)
                    self.x_buffer.append(index_X)
                    self.y_buffer.pop(0)
                    self.y_buffer.append(index_Y)

                    index_X = sum(self.x_buffer) / self.smoothening
                    index_Y = sum(self.y_buffer) / self.smoothening

                    pyautogui.moveTo(index_X, index_Y)
                    self.previous_x, self.previous_y = index_X, index_Y

            if (fingers[1] == 1 and fingers[2] == 1):
                length, _info, img = self.detector.findDistance(
                    hands[0]["lmList"][8], hands[0]["lmList"][12], frame)
                if (length < 40):
                    cv2.circle(frame, (_info[4], _info[5]),
                               15, (0, 255, 0), cv2.FILLED)
                    
                    pyautogui.click()

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)
