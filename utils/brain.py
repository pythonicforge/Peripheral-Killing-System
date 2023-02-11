import multiprocessing as mp

from utils.speech_synthesizer import Speak, Hear
from backend.brightness import GesturedBrightness


class Brain:
    def __init__(self) -> None:
        self.speaker = Speak(gender="female", language="english")

    def run(self) -> None:
        self.speaker.say("Initializing system!")

        audioOBJ = Hear()
        done = False

        is_brightness_turned_on, is_mode_active = False, False
        brightness_controller = mp.Process(target=GesturedBrightness)

        self.speaker.say("System initialization completed!")
        self.speaker.say("System is online and running!")

        while not done:
            response = audioOBJ.recognize_speech_from_mic()

            query = response["transcription"]
            if response["success"]:
                if (response["transcription"] != None):
                    query = query.lower().strip()
                    print(query)
                    if "exit" in query or "stop" in query:
                        done = True
                        self.speaker.say(
                            "Peripheral Killing System terminated. All systems are offline now!")
                    elif "brightness" and "on" in query:
                        if (is_mode_active == False):
                            if (is_brightness_turned_on == False):
                                is_brightness_turned_on, is_mode_active = True, True
                                brightness_controller.start()
                                self.speaker.say(
                                    "Brightness control mode turned on")
                            else:
                                self.speaker.say(
                                    "Brightness control mode is already turned on")
                        else:
                            self.speaker.say(
                                "Some other instances of control system are currently running! Please turn them off and try again later!")
                    elif "brightness" and "off" in query:
                        if (is_brightness_turned_on == True):
                            is_brightness_turned_on, is_mode_active = False, False
                            brightness_controller.terminate()
                            brightness_controller = mp.Process(
                                target=GesturedBrightness)
                            self.speaker.say(
                                "Brightness control mode turned off")
                        else:
                            self.speaker.say(
                                "No brightness control console is currently turned on. No actions taken!")

                    else:
                        pass
                elif query == None:
                    pass
