import multiprocessing as mp
import struct
import sys
import time

import pyaudio
import pvporcupine
import requests
from termcolor import colored

from utils.speech_synthesizer import Speak, Hear
from backend import *

class Brain:
    def __init__(self) -> None:
        self.speaker = Speak()

    def check_internet(self):
        url = 'http://www.google.com/'
        try:
            r = requests.get(url, timeout=3)
            return True
        except requests.ConnectionError:
            return False

    def run(self) -> None:
        """
        The run method initializes the system and listens to voice commands from the user. It uses Porcupine to detect the wake word "computer" and then listens for voice commands from the user.

        The method creates two processes, brightness_controller and volume_controller, which are used to control the brightness and volume of the computer respectively. These processes are started or terminated depending on the user's commands.

        The method also uses the Hear class to recognize speech from the user. The recognized speech is then processed by the system to perform various actions, such as turning on/off the brightness or volume control mode, putting the system to sleep, or exiting the program.

        The method loops until the user exits the program or puts the system to sleep.

        Parameters: None
        Returns: None
        """

        if self.check_internet() == False:
            self.speaker.say(
                "data/no_internet.mp3", "No internet connection available! Please connect to the internet in order to run this software!")
            sys.exit()
        else:
            self.speaker.say("data/init/1.mp3", "Initializing system!")

            audioOBJ = Hear()
            done = False

            is_brightness_turned_on, is_mode_active, is_volume_turned_on, is_mouse_turned_on, is_keyboard_turned_on = False, False, False, False, False
            brightness_controller, volume_controller, mouse_controller, keyboard_controller = mp.Process(
                target=GesturedBrightness), mp.Process(target=GesturedVolume), mp.Process(target=AirMouse), mp.Process(target=AirKeyboard)

            self.speaker.say("data/init/2.mp3",
                             "System initialization completed!")
            self.speaker.say("data/init/3.mp3",
                             "System is online and running!")
            time.sleep(1.5)
            self.speaker.say("data/awaitCall.mp3", "Awaiting your call!")

            porcupine = None
            p_audio = None
            audio_stream = None

            try:
                porcupine = pvporcupine.create(keywords=["computer"])
                p_audio = pyaudio.PyAudio()
                audio_stream = p_audio.open(
                    rate=porcupine.sample_rate,
                    channels=1,
                    format=pyaudio.paInt16,
                    input=True,
                    frames_per_buffer=porcupine.frame_length
                )

                while True:
                    pcm = audio_stream.read(porcupine.frame_length)
                    pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

                    keyword_index = porcupine.process(pcm)

                    if (keyword_index >= 0):

                        self.speaker.say("data/wake_system_up.mp3",
                                         "Hey! How can I help you?")
                        while not done:
                            response = audioOBJ.recognize_speech_from_mic()
                            query = response["transcription"]

                            if response["success"]:
                                if (response["transcription"] != None):
                                    query = query.lower().strip()
                                    print(
                                        colored(f"User: {query}", color="blue"))

                                    if "exit" in query or "stop"  in query:
                                        done = True
                                        if (is_brightness_turned_on == True):
                                            is_brightness_turned_on, is_mode_active = False, False
                                            brightness_controller.terminate()

                                        if (is_volume_turned_on == True):
                                            is_volume_turned_on, is_mode_active = False, False
                                            volume_controller.terminate()

                                        self.speaker.say("data/killSystem.mp3",
                                                         "Peripheral Killing System terminated. All systems are offline now!")
                                        sys.exit()

                                    elif "sleep" in query or "rest" in query or "deactivate" in query:
                                        if (is_brightness_turned_on == True):
                                            is_brightness_turned_on, is_mode_active = False, False
                                            brightness_controller.terminate()

                                        if (is_volume_turned_on == True):
                                            is_volume_turned_on, is_mode_active = False, False
                                            volume_controller.terminate()
                                        self.speaker.say(
                                            "data/hibernating_system.mp3", "Hibernating now! Call me when you need me!")
                                        break

                                    elif "turn on brightness mode" in query or "turn on brightness control mode" in query:
                                        if (is_mode_active == False):
                                            if (is_brightness_turned_on == False):
                                                is_brightness_turned_on, is_mode_active = True, True
                                                brightness_controller.start()
                                                self.speaker.say("data/brightness/brightness_on.mp3",
                                                                 "Brightness control mode turned on")
                                            else:
                                                self.speaker.say("data/brightness/brightness_already_on.mp3",
                                                                 "Brightness control mode is already turned on")
                                        else:
                                            self.speaker.say("data/other_system_on.mp3",
                                                             "Some other instances of control system are currently running! Please turn them off and try again later!")

                                    elif "turn off brightness mode" in query or "turn off brightness control mode" in query:
                                        if (is_brightness_turned_on == True):
                                            is_brightness_turned_on, is_mode_active = False, False
                                            brightness_controller.terminate()
                                            brightness_controller = mp.Process(
                                                target=GesturedBrightness)
                                            self.speaker.say("data/brightness/brightness_off.mp3",
                                                             "Brightness control mode turned off")
                                        else:
                                            self.speaker.say("data/brightness/no_brightness.mp3",
                                                             "No brightness control console is currently turned on. No actions taken!")

                                    elif "turn on volume mode" in query or "turn on volume control mode" in query:
                                        if (is_mode_active == False):
                                            if (is_volume_turned_on == False):
                                                is_volume_turned_on, is_mode_active = True, True
                                                volume_controller.start()
                                                self.speaker.say("data/volume/volume_on.mp3",
                                                                 "Volume control mode turned on")
                                            else:
                                                self.speaker.say("data/volume/volume_already_on.mp3",
                                                                 "Already switched to volume control mode")
                                        else:
                                            self.speaker.say("data/other_system_on.mp3",
                                                             "Some other instances of control system are currently running! Please turn them off and try again later!")

                                    elif "turn off volume mode" in query or "turn off volume control mode" in query:
                                        if (is_volume_turned_on == True):
                                            is_volume_turned_on, is_mode_active = False, False
                                            volume_controller.terminate()
                                            volume_controller = mp.Process(
                                                target=GesturedVolume)
                                            self.speaker.say(
                                                "data/volume/volume_off.mp3", "Turned off volume control mode")
                                        else:
                                            self.speaker.say("data/volume/no_volume.mp3",
                                                             "No volume control console is currently turned on. No actions taken")

                                    elif "turn on mouse mode" in query or "turn on mouse control mode" in query:
                                        if (is_mode_active == False):
                                            if (is_mouse_turned_on == False):
                                                is_mouse_turned_on, is_mode_active = True, True
                                                mouse_controller.start()
                                                self.speaker.say("data/mouse/mouse_on.mp3",
                                                                 "Mouse control mode turned on")
                                            else:
                                                self.speaker.say("data/mouse/mouse_already_on.mp3",
                                                                 "Mouse control mode is already turned on")
                                        else:
                                            self.speaker.say("data/other_system_on.mp3",
                                                             "Some other instances of control system are currently running! Please turn them off and try again later!")

                                    elif "turn off mouse mode" in query or "turn off mouse control mode" in query:
                                        if (is_mouse_turned_on == True):
                                            is_mouse_turned_on, is_mode_active = False, False
                                            mouse_controller.terminate()
                                            mouse_controller = mp.Process(
                                                target=AirMouse)
                                            self.speaker.say("data/mouse/mouse_off.mp3",
                                                             "Mouse control mode turned off")
                                        else:
                                            self.speaker.say("data/mouse/no_mouse.mp3",
                                                             "No mouse control console is currently turned on. No actions taken!")
                                    elif "turn on keyboard mode" in query or "turn on keyboard control mode" in query:
                                        if (is_mode_active == False):
                                            if (is_keyboard_turned_on == False):
                                                is_keyboard_turned_on, is_mode_active = True, True
                                                keyboard_controller.start()
                                                self.speaker.say("data/keyboard/keyboard_on.mp3",
                                                                 "Keyboard control mode turned on")
                                            else:
                                                self.speaker.say("data/keyboard/keyboard_already_on.mp3",
                                                                 "Keyboard control mode is already turned on")
                                        else:
                                            self.speaker.say("data/other_system_on.mp3",
                                                             "Some other instances of control system are currently running! Please turn them off and try again later!")

                                    elif "turn off keyboard mode" in query or "turn off keyboard control mode" in query:
                                        if (is_keyboard_turned_on == True):
                                            is_keyboard_turned_on, is_mode_active = False, False
                                            keyboard_controller.terminate()
                                            keyboard_controller = mp.Process(
                                                target=AirMouse)
                                            self.speaker.say("data/keyboard/keyboard_off.mp3",
                                                             "Keyboard control mode turned off")
                                        else:
                                            self.speaker.say("data/keyboard/no_keyboard.mp3",
                                                             "No keyboard control console is currently turned on. No actions taken!")
                                    else:
                                        pass
                                elif query == None:
                                    pass
                        time.sleep(0.5)
                        self.speaker.say("data/awaitCall.mp3",
                                         "Awaiting your call!")

            finally:
                if porcupine is not None:
                    porcupine.delete()

                if audio_stream is not None:
                    audio_stream.close()

                if p_audio is not None:
                    p_audio.terminate()
