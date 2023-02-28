import subprocess
import wolframalpha
import pyttsx3
import tkinter
import json
import requests
from ecapture import ecapture as ec
import random
import operator
import speech_recognition as sr
import datetime
import wikipedia
import webbrowser
import os
import webbrowser
import winshell
import pyjokes
import datetime 
import feedparser
import smtplib
import ctypes
import time
import requests
import shutil
from twilio.rest import Client
from clint.textui import progress
from ecapture import ecapture as ec
from bs4 import BeautifulSoup
import win32com.client as wincl
from urllib.request import urlopen


def speak_engine(audio):
    time.sleep(0.6)
    engine = pyttsx3.init()
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume - 0.25)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', rate + 100)
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[0].id)
    engine.say(audio) 
    engine.runAndWait()

def Greetings():
    hours = int(datetime.datetime.now().hour)
    if hours >= 0 and hours < 12:
        speak_engine('good morning')
    elif hours >= 12 and hours < 18:
        speak_engine('good afternoon')
    elif hours >= 18 and hours < 24:
        speak_engine('good evening')
    else:
        speak_engine('good night')
    time.sleep(0.10)
    speak_engine('i am artificial intelligence created')
    
def takeCommand():
    r = sr.Recognizer()
     
    with sr.Microphone() as source:
         
        print("listening...")
        r.pause_threshold = 0.7
        audio = r.listen(source)
  
    try:
        print("recognizing...")   
        query = r.recognize_google(audio, language ='en-us')
        print(f"User said: {query}\n")
  
    except Exception as e:
        print(e)   
        print("unable to recognize your voice.") 
        return "none"
     
    return query

def TellTime(self):
    time = datetime.datetime.now().strftime("%I:%M:%S")
    print(time)
    hour = int(datetime.datetime.now().hour)
    min = int(datetime.datetime.now().minute)
    self.speak_engine(self,f"The time is {hour}:{min}")

def TellDate():
    day = datetime.datetime.today().weekday()
    day_dict = {1:'Monday',2:'Tuesday',3:'Wednesday',4:'Thursday',5:'Friday',6:'Saturday',7:'Sunday'}
    if day in day_dict.keys():
        day_of_week = day_dict[day]
        print(day_of_week)
        speak_engine(f"Today is {day_of_week}")
        
if __name__ == '__main__':
    clear = lambda: os.system('cls' if os.name == 'nt' else 'clear')
    clear()
    Greetings()
    while True:
        
        time.sleep(0.15)
        speak_engine("so tell me how would Be able to assist you?")
        
        query = takeCommand().lower()
        
        if 'wikipedia' in query:
            speak_engine('searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary(query, sentences=2)
            speak_engine("according to wikipedia")
            print(results)
            speak_engine(results)
        
        elif 'open youtube' in query:
            speak_engine('opening youtube...')
            webbrowser.open('youtube.com')
            
        elif 'what time is it' in query or 'time' in query:
            strime = datetime.datetime.now().strftime("%I:%M:%S")
            speak_engine(f"the time is {strime}")
            
        elif 'i have a question about computational' in query or 'i have a question about geographical' in query:
            speak_engine("this is a simple bot that allows you to ask computational and geographical questions. Please tell me your question, and I will try to answer it.")
            question = takeCommand().lower()
            app_id = "PW765U-K9P296J7YW"
            client = wolframalpha.Client(app_id)
            res = client.query(question)
            answer = next(res.results).text
            speak_engine(answer)
            print(answer)
        
        elif 'what is the forecast today' in query:
            api_key = '72e5c56e6d21549b6840d8965b6fa72a'
            base_url = 'https://api.openweathermap.org/data/3.0/weather?'
            speak_engine('what is the name of the city')
            city_name = takeCommand().lower()
            complete_url = base_url + 'appid=' + api_key + '&q=' +city_name
            response = requests.get(complete_url)
            x=response.json()
            if x['status'] != '400':
                y=x['main']
                current_temperature = y['temp']
                current_humidiy = y['humidity']
                z=x['weather']
                weather_description = z[0]['description']
                speak_engine('temperature is ' + str(current_temperature + '°C') + ' degrees'+'\n humidity is ' + str(current_humidiy) + '%'+ '\n description is ' + str(weather_description))
                print('temperature is ' + str(current_temperature + '°C') + ' degrees'+'\n humidity is ' + str(current_humidiy) + '%'+ '\n description is ' + str(weather_description))
                
        elif 'search' in query or 'find' in query:
            query = query.replace("search","")
            webbrowser.open(f"https://www.google.com/search?q={query}")
            time.sleep(3)
        
        elif 'close' in query or 'exit' in query:
            speak_engine('bye. hope to hear from you soon.')
            exit()