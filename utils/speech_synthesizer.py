import pygame
import os

def speak_audio(text, voice="en-US-EricNeural", female=False, english=True):
    language_support = {
        "Male English": "en-US-EricNeural",
        "Female English": "en-US-AriaNeural",
        "Male Hindi": "hi-IN-MadhurNeural",
        "Female Hindi": "hi-IN-SwaraNeural",
    }

    if(female == True):
        if(english == False):
            voice = language_support["Female Hindi"]
        else:
            voice = language_support["Female English"]
    else:
        if(english == False):
            voice = language_support["Male Hindi"]
        else:
            voice = language_support["Male English"]

    command = f'edge-tts --voice "{voice}" --text "{text}" --write-media "data.mp3"'

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