import multiprocessing as mp

from termcolor import colored

from utils.speech_synthesizer import Speak, Hear
from backend.brightness import GesturedBrightness
from backend.volume import GesturedVolume


class Brain:
    def __init__(self) -> None:
        self.speaker = Speak(gender="female", language="english")

    def run(self) -> None:
        self.speaker.say("Initializing system!")

        audioOBJ = Hear()
        done = False

        is_brightness_turned_on, is_mode_active = False, False
        brightness_controller, volume_controller = mp.Process(
            target=GesturedBrightness), mp.Process(target=GesturedVolume)

        self.speaker.say("System initialization completed!")
        self.speaker.say("System is online and running!")

        while not done:
            response = audioOBJ.recognize_speech_from_mic()
            query = response["transcription"]

            if response["success"]:
                if (response["transcription"] != None):
                    query = query.lower().strip()
                    print(colored(f"User: {query}", color="blue"))

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
                                
                    elif "volume" and "on" in query:
                        if (is_mode_active == False):
                            if (is_volume_turned_on == False):
                                is_volume_turned_on, is_mode_active = True, True
                                volume_controller.start()
                                self.speaker.say(
                                    "Volume control mode turned on")
                            else:
                                self.speaker.say(
                                    "Already switched to volume control mode")
                        else:
                            self.speak_audio(
                                "Some other instances of control system are currently running! Please turn them off and try later!")

                    elif "volume" and "off" in query:
                        if (is_volume_turned_on == True):
                            is_volume_turned_on, is_mode_active = False, False
                            volume_controller.terminate()
                            volume_controller = mp.Process(
                                target=GesturedVolume)
                            self.speaker.say("Turned off volume control mode")
                        else:
                            self.speaker.say(
                                "No volume control console is currently turned on. No actions taken")

                    else:
                        pass
                elif query == None:
                    pass
