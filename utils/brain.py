import multiprocessing as mp
import struct
import sys
import time

import pyaudio
import pvporcupine
from termcolor import colored

from utils.speech_synthesizer import Speak, Hear
import backend


class Brain:
    def __init__(self) -> None:
        self.speaker = Speak()

    def run(self) -> None:
        self.speaker.say("data/initialisation1.mp3", "Initializing system!")

        audioOBJ = Hear()
        done = False

        is_brightness_turned_on, is_mode_active, is_volume_turned_on = False, False, False
        brightness_controller, volume_controller = mp.Process(
            target=backend.GesturedBrightness), mp.Process(target=backend.GesturedVolume)

        self.speaker.say("data/initialisation2.mp3",
                         "System initialization completed!")
        self.speaker.say("data/initialisation3.mp3",
                         "System is online and running!")
        time.sleep(1.5)
        self.speaker.say("data/sleep2.mp3", "Awaiting your call!")

        porcupine = None
        p_audio = None
        audio_stream = None

        try:
            porcupine = pvporcupine.create(keywords=["computer", "jarvis"])
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

                    self.speaker.say("data/sleep3.mp3",
                                     "Hey! How can I help you?")
                    while not done:
                        response = audioOBJ.recognize_speech_from_mic()
                        query = response["transcription"]

                        if response["success"]:
                            if (response["transcription"] != None):
                                query = query.lower().strip()
                                print(colored(f"User: {query}", color="blue"))

                                if "exit" in query or "stop" in query:
                                    done = True
                                    if (is_brightness_turned_on == True):
                                        is_brightness_turned_on, is_mode_active = False, False
                                        brightness_controller.terminate()

                                    if (is_volume_turned_on == True):
                                        is_volume_turned_on, is_mode_active = False, False
                                        volume_controller.terminate()

                                    self.speaker.say("data/kill.mp3",
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
                                        "data/sleep1.mp3", "Hibernating now! Call me when you need me!")
                                    break

                                elif "turn on brightness mode" in query or "turn on brightness control mode" in query:
                                    if (is_mode_active == False):
                                        if (is_brightness_turned_on == False):
                                            is_brightness_turned_on, is_mode_active = True, True
                                            brightness_controller.start()
                                            self.speaker.say("data/brightness_on.mp3",
                                                             "Brightness control mode turned on")
                                        else:
                                            self.speaker.say("data/brightness_already_on.mp3",
                                                             "Brightness control mode is already turned on")
                                    else:
                                        self.speaker.say("data/other_system_on.mp3",
                                                         "Some other instances of control system are currently running! Please turn them off and try again later!")

                                elif "turn off brightness mode" in query or "turn off brightness control mode" in query:
                                    if (is_brightness_turned_on == True):
                                        is_brightness_turned_on, is_mode_active = False, False
                                        brightness_controller.terminate()
                                        brightness_controller = mp.Process(
                                            target=backend.GesturedBrightness)
                                        self.speaker.say("data/brightness_off.mp3",
                                                         "Brightness control mode turned off")
                                    else:
                                        self.speaker.say("data/no_brightness.mp3",
                                                         "No brightness control console is currently turned on. No actions taken!")

                                elif "turn on volume mode" in query or "turn on volume control mode" in query:
                                    if (is_mode_active == False):
                                        if (is_volume_turned_on == False):
                                            is_volume_turned_on, is_mode_active = True, True
                                            volume_controller.start()
                                            self.speaker.say("data/volume_on.mp3",
                                                             "Volume control mode turned on")
                                        else:
                                            self.speaker.say("data/volume_already_on.mp3",
                                                             "Already switched to volume control mode")
                                    else:
                                        self.speaker.say("data/other_system_on.mp3",
                                                         "Some other instances of control system are currently running! Please turn them off and try again later!")

                                elif "turn off volume mode" in query or "turn off volume control mode" in query:
                                    if (is_volume_turned_on == True):
                                        is_volume_turned_on, is_mode_active = False, False
                                        volume_controller.terminate()
                                        volume_controller = mp.Process(
                                            target=backend.GesturedVolume)
                                        self.speaker.say(
                                            "data/volume_off.mp3", "Turned off volume control mode")
                                    else:
                                        self.speaker.say("data/no_volume.mp3",
                                                         "No volume control console is currently turned on. No actions taken")

                                else:
                                    pass
                            elif query == None:
                                pass
                    time.sleep(1.5)
                    self.speaker.say("data/sleep2.mp3", "Awaiting your call!")

        finally:
            if porcupine is not None:
                porcupine.delete()

            if audio_stream is not None:
                audio_stream.close()

            if p_audio is not None:
                p_audio.terminate()
