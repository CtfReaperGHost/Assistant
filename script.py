import openai
import os
from dotenv import load_dotenv
from datetime import datetime
import speech_recognition as sr
import pyttsx3
import webbrowser
import wikipedia
import wolframalpha
import google.cloud.texttospeech as tts
import pygame
import time
from ctypes import *
# Load credentials
load_dotenv()

### PARAMETERS ###
activationWords = ['computer', 'calcutron', 'shodan', 'showdown']
tts_type = 'google' # google or local

#Creating the engine
engine = pyttsx3.init()
engine.setProperty('voice', voices[0].id)
engine.say(audio) 

# Wolfram Alpha client
appId = '5R49J7-J888YX9J2V'
wolframClient = wolframalpha.Client(appId)

# Google TTS client
def google_text_to_wav(voice_name: str, text: str):
    language_code = "-".join(voice_name.split("-")[:2])

    # Set the text input to be synthesized
    text_input = tts.SynthesisInput(text=text)

    # Build the voice request, select the language code ("en-US") and the voice name
    voice_params = tts.VoiceSelectionParams(
        language_code=language_code, name=voice_name
    )

    # Select the type of audio file you want returned
    audio_config = tts.AudioConfig(audio_encoding=tts.AudioEncoding.LINEAR16)

    client = tts.TextToSpeechClient()
    response = client.synthesize_speech(
        input=text_input, voice=voice_params, audio_config=audio_config
    )

    return response.audio_content

#Create the ai speaker object
def speak(text, rate = 120):
    time.sleep(0.3)

    if tts_type == 'local':
        engine.setProperty('rate', rate) 
        engine.say(text)
        engine.runAndWait()
    if tts_type == 'google':
        speech = google_text_to_wav('en-US-News-K', text)
        pygame.mixer.init(frequency=12000, buffer = 512)
        speech_sound = pygame.mixer.Sound(speech)
        speech_sound.play()
        time.sleep(len(text.split()))
        pygame.mixer.quit()

# Configure browser
# Set the path
firefox_path = r"browser path"
# Register the browser
webbrowser.register('firefox', None, 
                    webbrowser.BackgroundBrowser(firefox_path))

def Greetings():
    hour=datetime.datetime.now().hour
    if hour>=0 and hour<12:
        speak("Hello,Good Morning")
        print("Hello,Good Morning")
    elif hour>=12 and hour<18:
        speak("Hello,Good Afternoon")
        print("Hello,Good Afternoon")
    else:
        speak("Hello,Good Evening")
        print("Hello,Good Evening")

def takeCommand():
        listener = sr.Recognizer()
        print('Listening...')

        with sr.Microphone() as source:
            listener.pause_threshold = 2
            input_speech = listener.listen(source)

        try:
            print('Recognizing...')
            query = listener.recognize_google(input_speech, language='en_us')
            print(f'The input speech was: {query}')

        except Exception as exception:
            print('Unable to Recognize your voice.')
            print(exception)
            return 'None'
        return query

def search_wikipedia(keyword=''):
    searchResults = wikipedia.search(keyword)
    if not searchResults:
        return 'No result received'
    try: 
        wikiPage = wikipedia.page(searchResults[0]) 
    except wikipedia.DisambiguationError as error:
        wikiPage = wikipedia.page(error.options[0])
    print(wikiPage.title)
    wikiSummary = str(wikiPage.summary)
    return wikiSummary

def listOrDict(var):
    if isinstance(var, list):
        return var[0]['plaintext']
    else:
        return var['plaintext']


def search_wolframalpha(keyword=''):
    response = wolframClient.query(keyword)
    # Query not resolved
    if response['@success'] == 'false':
        speak('I could not compute')
    # Query resolved
    else: 
        result = ''
        # Question
        pod0 = response['pod'][0]
        # May contain answer (Has highest confidence value) 
        # if it's primary or has the title of result or definition, then it's the official result
        pod1 = response['pod'][1]
        if (('result') in pod1['@title'].lower()) or (pod1.get('@primary', 'false') == 'true') or ('definition' in pod1['@title'].lower()):
            # Get the result
            result = listOrDict(pod1['subpod'])
            # Remove bracketed section
            return result.split('(')[0]
        else:
            # Get the interpretation from pod0
            question = listOrDict(pod0['subpod'])
            # Remove bracketed section
            question = question.split('(')[0]
            # Could search wiki instead here? 
            return question

def query_openai(prompt = ""):
    openai.organization = os.environ['api_org']
    openai.api_key = os.environ['api_key']
    # Temperature is a measure of randonmess
    # Max_tokens is the number of tokens to generate
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        temperature=0.3,
        max_tokens=80,
    )

    return response.choices[0].text


#main Loop
if __name__ == "__main__":
    speak("Hello, Welcome to my Assistant")
    while True:
        query = takeCommand().lower().split()
        if query[0] in activationWords and len(query) > 1:
            query.pop(0)
            # Set commands
            if query[0] == 'say':
                if 'hello' in query:
                    speak('Greetings, all!')
                else:
                    query.pop(0) # Remove 'say'
                    speech = ' '.join(query) 
                    speak(speech)
            
            # query openai
            if query[0] == 'insight':
                query.pop(0) # Remove 'insight'
                query = ' '.join(query)
                speech = query_openai(query)
                speak("Ok")
                speak(speech)
            
            # Navigation
            if query[0] == 'go' and query[1] == 'to':
                speak('Opening... ')
                # Assume the structure is activation word + go to, so let's remove the next two words
                query = ' '.join(query[2:])
                webbrowser.get('chrome').open_new(query)

            # Wikipedia
            if query[0] == 'wikipedia':
                query = ' '.join(query[1:])
                speak('Querying the universal databank')
                time.sleep(2)
                speak(search_wikipedia(query))

            # Wolfram Alpha
            if query[0] == 'compute' or query[0] == 'computer':
                query = ' '.join(query[1:])
                try:
                    result = search_wolframalpha(query)
                    speak(result)
                except:
                    speak('Unable to compute')

            # Note taking
            if query[0] == 'log':
                speak('Ready to record your note')
                newNote = parseCommand().lower()
                now = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
                with open('note_%s.txt' % now, 'w') as newFile:
                    newFile.write(now)
                    newFile.write(' ')
                    newFile.write(newNote)
                speak('Note written')

            if query[0] == 'exit':
                speak('Goodbye')
                break