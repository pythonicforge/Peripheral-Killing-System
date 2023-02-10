import os
import nltk
from neuralintents import GenericAssistant
from termcolor import colored

from utils.speech_synthesizer import speak_audio

def run():
    speak_audio("Initializing system")
    PATH = f'{os.getcwd()}\data'

    nltk.data.path = [PATH]
    print(colored(f'PATHS found: {nltk.data.path}', "green"))
    try:
        nltk.download('punkt', download_if_missing=True)
        nltk.download('wordnet', download_if_missing=True)
    except Exception as e:
        print(colored("The 'punkt' and 'wordnet' data package already exists.", "yellow"))

    assistant = GenericAssistant('intents.json', model_name="test_model")
    assistant.train_model()
    assistant.save_model()

    done = False
    speak_audio("System initialization completed")

    while not done:
        message = input("Enter a message: ")
        if message == "exit":
            done = True
        else:
            transcript = assistant.request(message)
            print(transcript)
            speak_audio(transcript) 