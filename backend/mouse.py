import tkinter as tk
import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import ImageTk, Image
import pyautogui


class AirMouse:
    def __init__(self):

        self.window = tk.Tk()
        self.screen = (self.window.winfo_screenwidth(),
                       self.window.winfo_screenheight())
        self.window.title("Mouse Control Console")
        self.window.geometry("640x480")
        self.window.resizable(False, False)

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.5, maxHands=1)

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def frame_to_screen_position(self, frame_dimensions, screen_dimensions=None, frame_position=None):
        screen_dimensions = self.screen
        x, y = screen_dimensions[1] / \
            frame_dimensions[0], screen_dimensions[0]/frame_dimensions[1]
        screen_position = [frame_position[0]*x, frame_position[1]*y]

        return screen_position

    def euclidean_distance(self, pt1, pt2):
        distance = np.sqrt((pt2[0] - pt1[0])**2 + (pt2[1] - pt1[1])**2)

        return distance

    def update(self):
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)

        hands, frame = self.detector.findHands(
            frame, draw=True, flipType=False)

        if hands is not None and len(hands) > 0:
            handLms = hands[0]["indexCoords"]

            if handLms is not None:
                frame_dimensions = frame.shape[:2][::-1]
                screen_pos = self.frame_to_screen_position(
                    frame_dimensions, self.screen, handLms)

                if screen_pos is not None:
                    pyautogui.moveTo(screen_pos[0], screen_pos[1])

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)


if __name__ == '__main__':
    AirMouse()
