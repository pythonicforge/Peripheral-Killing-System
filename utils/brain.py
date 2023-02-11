import os
import nltk
from neuralintents import GenericAssistant
from termcolor import colored

from utils.speech_synthesizer import Speak, Hear


class Brain:
    def __init__(self) -> None:
        self.speaker = Speak(female=True, english=True)

    def run(self):
        self.speaker.say("Initializing system!")
        PATH = f'{os.getcwd()}\data'

        nltk.data.path = [PATH]
        print(colored(f'PATHS found: {nltk.data.path}', "green"))
        try:
            nltk.download('punkt', download_if_missing=True)
            nltk.download('wordnet', download_if_missing=True)
        except Exception as e:
            print(
                colored("The 'punkt' and 'wordnet' data package already exists.", "yellow"))

        assistant = GenericAssistant('intents.json')
        assistant.train_model()
        assistant.save_model()

        object = Hear()
        done = False

        self.speaker.say("System initialization completed!")
        self.speaker.say("System is online and running!")

        while not done:
            response = object.recognize_speech_from_mic()
            
            query = response["transcription"]
            if response["success"]:
                if(response["transcription"] != None):
                    query = query.lower().strip()
                    print(query)
                    if query == "exit":
                        done = True
                        self.speaker.say("Peripheral Killing System terminated. All systems are offline now!")
                    else:
                        transcript = assistant.request(query)
                        print(transcript)
                        self.speaker.say(transcript)
                elif query == None:
                    pass
                    
            else:
                self.speaker.say("I'm sorry, I had trouble hearing you.")
