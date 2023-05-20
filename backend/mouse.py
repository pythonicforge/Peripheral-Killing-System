import tkinter as tk
import autopy
import cv2
import mediapipe
import numpy
from PIL import ImageTk, Image


class AirMouse:
    def __init__(self):
        """Initializes the AirMouse class.

        This constructor sets up the GUI window, video capture, hand tracking module, and other necessary variables.
        """

        self.window = tk.Tk()
        self.screen = (
            self.window.winfo_screenwidth(),
            self.window.winfo_screenheight(),
        )

        self.window.title("Mouse Control Console")
        self.window.geometry("640x480")
        self.window.resizable(False, False)

        self.cap = cv2.VideoCapture(0)

        self.initHand = mediapipe.solutions.hands
        self.mainHand = self.initHand.Hands(
            min_detection_confidence=0.6, min_tracking_confidence=0.6
        )
        self.draw = mediapipe.solutions.drawing_utils
        (
            self.wScr,
            self.hScr,
        ) = autopy.screen.size()
        self.pX, self.pY = 0, 0
        self.cX, self.cY = 0, 0

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def handLandmarks(self, colorImg, img):
        """Detects and tracks hand landmarks in the given color image.

        Args:
            colorImg (numpy.ndarray): The input color image.
            img (numpy.ndarray): The image on which to draw the hand landmarks.

        Returns:
            list: A list of landmark positions, each represented as [index, centerX, centerY].
        """
        landmarkList = []

        landmarkPositions = self.mainHand.process(colorImg)
        landmarkCheck = landmarkPositions.multi_hand_landmarks
        if landmarkCheck:
            for hand in landmarkCheck:
                for index, landmark in enumerate(hand.landmark):
                    self.draw.draw_landmarks(img, hand, self.initHand.HAND_CONNECTIONS)
                    h, w, c = img.shape
                    centerX, centerY = int(landmark.x * w), int(landmark.y * h)
                    landmarkList.append([index, centerX, centerY])

        return landmarkList

    def fingers(self, landmarks, lmList):
        """Determines the state of the fingers based on the landmark positions.

        Args:
            landmarks (list): A list of landmark positions, each represented as [index, centerX, centerY].
            lmList (list): The complete list of hand landmarks.

        Returns:
            list: A list of binary values indicating the state of each finger.
        """
        fingerTips = []
        tipIds = [4, 8, 12, 16, 20]

        if landmarks[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingerTips.append(1)
        else:
            fingerTips.append(0)

        for id in range(1, 5):
            if landmarks[tipIds[id]][2] < landmarks[tipIds[id] - 3][2]:
                fingerTips.append(1)
            else:
                fingerTips.append(0)

        return fingerTips

    def update(self):
        """Updates the air mouse control.

        This method is called periodically to capture video frames, process hand landmarks, and control the mouse cursor
        based on finger states.
        """
        check, img = self.cap.read()
        img = cv2.flip(img, 1)
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        lmList = self.handLandmarks(imgRGB, img)

        if len(lmList) != 0:
            x1, y1 = lmList[8][1:]
            x2, y2 = lmList[12][1:]
            finger = self.fingers(lmList, lmList)

            if finger[1] == 1 and finger[2] == 0:
                x3 = numpy.interp(x1, (75, 640 - 75), (0, self.wScr))
                y3 = numpy.interp(y1, (75, 480 - 75), (0, self.hScr))

                self.cX = self.pX + (x3 - self.pX) / 7
                self.cY = self.pY + (y3 - self.pY) / 7

                autopy.mouse.move(self.wScr - self.cX, self.cY)
                self.pX, self.pY = (
                    self.cX,
                    self.cY,
                )

            if finger[1] == 0 and finger[0] == 1:
                autopy.mouse.click()

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        if check:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)
