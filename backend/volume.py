from comtypes import CLSCTX_ALL
from ctypes import cast, POINTER
import tkinter as tk

import cv2
from cvzone.HandTrackingModule import HandDetector
import numpy as np
from PIL import ImageTk, Image
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume


class GesturedVolume:
    def __init__(self):
        """
        Initializes the GesturedVolume object, which creates the GUI window and initializes the necessary objects and variables for volume control. The method starts the main event loop for the GUI window.
        """

        self.window = tk.Tk()
        self.window.title("Volume Control Console")

        self.cap = cv2.VideoCapture(0)
        self.detector = HandDetector(detectionCon=0.5, maxHands=1)

        self.devices = AudioUtilities.GetSpeakers()
        self.interface = self.devices.Activate(
            IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume = cast(self.interface, POINTER(IAudioEndpointVolume))

        self.volRange, self.volPer = self.volume.GetVolumeRange(), 0
        self.minVol, self.maxVol = self.volRange[0], self.volRange[1]

        self.canvas = tk.Canvas(self.window, width=640, height=480)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        """
        Updates the GUI window by reading a frame from the video capture device, detecting the user's hand and fingers using a HandDetector object, and adjusting the system volume based on the position of the user's fingers. The method then displays the current system volume and hand detection results on the video frame, and updates the GUI window with the new video frame. This method is called repeatedly by the mainloop() of the GUI window.
        """

        ret, frame = self.cap.read()

        cv2.putText(frame, f"VOLUME: {round(self.volume.GetMasterVolumeLevelScalar()*100)}%", (
            40, 50), cv2.FONT_HERSHEY_PLAIN, 2, (2, 0, 63), 2)

        hands, frame = self.detector.findHands(frame, draw=True, flipType=True)
        if hands:
            if (len((hands[0]["lmList"])) != 0):
                fingers = self.detector.fingersUp(hands[0])

                if (fingers[0] == 1 and fingers[1] == 1):
                    length, info, frame = self.detector.findDistance(
                        hands[0]["lmList"][4], hands[0]["lmList"][8], frame)
                    vol = np.interp(length, [50, 300], [
                                    self.minVol, self.maxVol])
                    self.volPer = np.interp(length, [50, 300], [0, 100])
                    self.volume.SetMasterVolumeLevel(int(vol), None)

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)

        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)
