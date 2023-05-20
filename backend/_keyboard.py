import time
import tkinter as tk
import cv2
from cvzone.HandTrackingModule import HandDetector
from PIL import ImageTk, Image
from pynput.keyboard import Controller, Key


class AirKeyboard:
    def __init__(self):
        """Initialize the AirKeyboard application.

        Sets up the main GUI window, video capture, hand detector, keyboard controller,
        and button layout. Starts the main event loop for the application.
        """
        self.window = tk.Tk()
        self.screen = (
            self.window.winfo_screenwidth(),
            self.window.winfo_screenheight(),
        )

        self.window.title("Keyboard Control Console")
        self.window.geometry("1280x720")
        self.window.resizable(False, False)

        self.cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        self.cap.set(3, 1280)
        self.cap.set(4, 720)

        self.detector = HandDetector(detectionCon=0.7, maxHands=1)

        self.keys = [
            ["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"],
            ["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
            ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
            ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"],
        ]
        self.keyboard = Controller()

        self.buttonList = []

        for i in range(len(self.keys)):
            for x, key in enumerate(self.keys[i]):
                self.buttonList.append(Button([100 * x + 50, 100 * i + 50], key))

        self.buttonList.append(Button((50, 450), "Spacebar", [580, 90]))

        self.buttonList.append(Button((650, 450), "Backspace", [400, 90]))

        self.canvas = tk.Canvas(self.window, width=1280, height=720)
        self.canvas.pack()

        self.delay = 15
        self.update()

        self.window.mainloop()

    def update(self):
        """Update the GUI and process hand gestures.

        Continuously captures video frames, detects hands, and highlights and presses
        the corresponding buttons based on hand gestures. Updates the GUI with the
        processed frames.
        """
        check, img = self.cap.read()
        img = cv2.flip(img, 1)

        hands, img = self.detector.findHands(img, draw=True, flipType=False)

        img = self.drawAll(img, self.buttonList)

        if hands:
            if len((hands[0]["lmList"])) != 0:
                for button in self.buttonList:
                    x, y = button.position
                    w, h = button.size

                    if (
                        x < hands[0]["lmList"][8][0] < x + w
                        and y < hands[0]["lmList"][8][1] < y + h
                    ):
                        cv2.rectangle(
                            img,
                            button.position,
                            (x + w, y + h),
                            (86, 0, 139),
                            cv2.FILLED,
                        )
                        cv2.putText(
                            img,
                            button.text,
                            (button.position[0] + 20, button.position[1] + 65),
                            cv2.FONT_HERSHEY_SIMPLEX,
                            2,
                            (255, 255, 255),
                            2,
                        )
                        length, _, _ = self.detector.findDistance(
                            hands[0]["lmList"][8], hands[0]["lmList"][12], img
                        )
                        if length < 35:
                            if button.text == "Backspace":
                                self.keyboard.press(Key.backspace)
                                self.keyboard.release(Key.backspace)
                            elif button.text == "Spacebar":
                                self.keyboard.press(Key.space)
                                self.keyboard.release(Key.space)
                            else:
                                self.keyboard.press(button.text)
                            cv2.rectangle(
                                img,
                                button.position,
                                (x + w, y + h),
                                (0, 255, 0),
                                cv2.FILLED,
                            )
                            cv2.putText(
                                img,
                                button.text,
                                (button.position[0] + 20, button.position[1] + 65),
                                cv2.FONT_HERSHEY_SIMPLEX,
                                2,
                                (255, 255, 255),
                                2,
                            )
                            time.sleep(0.2)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)

        if check:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(img))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def drawAll(self, img, buttonList):
        """Draw all buttons on the image.

        Args:
            img: The image to draw buttons on.
            buttonList: A list of Button objects representing the buttons to be drawn.

        Returns:
            The image with buttons drawn.
        """
        for button in buttonList:
            x, y = button.position
            w, h = button.size
            cv2.rectangle(
                img, button.position, (x + w, y + h), (159, 1, 255), cv2.FILLED
            )
            cv2.putText(
                img,
                button.text,
                (button.position[0] + 20, button.position[1] + 65),
                cv2.FONT_HERSHEY_SIMPLEX,
                2,
                (255, 255, 255),
                2,
            )
        return img


class Button:
    def __init__(self, position, text, size=[85, 85]):
        """Initialize a button object.

        Args:
            position: The position of the button as a tuple (x, y).
            text: The text label of the button.
            size: The size of the button as a list [width, height].
        """

        self.position = position
        self.text = text
        self.size = size


AirKeyboard()
