import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests, json, os, time
import pygame
import datetime
import schedule
from gtts import gTTS
from time import sleep


def xml_speech():
    print("Time being played: " + str(datetime.datetime.now().strftime("%I:%M %p")))
    pygame.mixer.init()
    pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue


def calculate_next_interval():
    now = datetime.datetime.now()
    minutes = now.minute

    next_interval = datetime.datetime(now.year, now.month, now.day, now.hour, minutes + 5 - ((minutes +1)% 5))

    return next_interval

def wait_until_next_interval():
    next_interval = calculate_next_interval()
    time_difference = (next_interval - datetime.datetime.now()).total_seconds()

    if time_difference > 0:
        time.sleep(time_difference)

# Schedule the program to run every 5 minutes
schedule.every(5).minutes.do(xml_speech)

if __name__ == "__main__":
    # Calculate and wait until the next interval
    print("Time: " + str(datetime.datetime.now().strftime("%I:%M %p")))
    
    wait_until_next_interval()

    # Run the program immediately
    xml_speech()

    # Continuously run the schedule
    while True:
        schedule.run_pending()
        time.sleep(1)
