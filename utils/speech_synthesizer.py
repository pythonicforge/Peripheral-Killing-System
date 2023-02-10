import pygame
import os


class Speak:
    def __init__(self, voice="en-US-EricNeural", female=False, english=True) -> None:

        self.voice = voice
        self.gender = female
        self.language = english

        language_support = {
            "Male English": "en-US-EricNeural",
            "Female English": "en-US-AriaNeural",
            "Male Hindi": "hi-IN-MadhurNeural",
            "Female Hindi": "hi-IN-SwaraNeural",
        }

        if (self.gender == True):
            if (self.language == False):
                self.voice = language_support["Female Hindi"]
            else:
                self.voice = language_support["Female English"]
        else:
            if (self.language == False):
                self.voice = language_support["Male Hindi"]
            else:
                self.voice = language_support["Male English"]

    def say(self, text):

        command = f'edge-tts --voice "{self.voice}" --text "{text}" --write-media "data.mp3"'

        os.system(command)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load("data.mp3")

        try:
            pygame.mixer.music.play()

            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)

        except Exception as e:
            print(e)

        finally:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
            os.remove("data.mp3")
