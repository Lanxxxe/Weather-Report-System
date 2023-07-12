import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests
import json
import os
import time
import RPi.GPIO as GPIO
import pygame
import datetime
from gtts import gTTS
from time import sleep

'''
Tacloban City
Temperature: 69 degrees
Chance of rain: 69%
Humidity: 69%
'''

'''
OUTPUTS
-Time
-Weather Forecast (Location, Temperature, Chance of Rain, Humidity)
-Alert (Auto play if meron)
-With 30 minutes Interval (Nearest 30 minutes [':00' || ':30'])
-Button [1] - Weather Forecast with current time
-Button [2] - Time => Today is July 10, 2023. The time is 5:26pm
'''

class Weather:
    '''Initializing'''
    def __init__(self, api_location, api_key):
        self.location = api_location
        self.key = api_key
        self.accuweather_url = requests.get('http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=1&aqi=yes&alerts=yes'.format(self.key, self.location))
        self.accuweather_url.raise_for_status
        self.weather_response = json.loads(self.accuweather_url.text)
    
    def weather_data(self):
        '''Getting some information on WeatherAPI as Dictionary'''
        self.weather_information = {
            "Today-is": str(datetime.datetime.now().strftime("%B %d %Y. The time is %I:%M %p")),
            "Weather-Report-in" : self.weather_response['location']['name'],
            "Temperature" : '{} degrees'.format(self.weather_response['current']['temp_c']),
            "Humidity" : '{} percent'.format(self.weather_response['current']['humidity']),
            "Chance-Of-Rain" : '{} percent'.format(self.weather_response['forecast']['forecastday'][0]['day']['daily_chance_of_rain'])
        }   
        return self.weather_information

    def xml_data(self): 
        #Weather_Data as root of the XML file
        self.xml_title = ET.Element('Weather_Data')

        for keys, values in self.weather_data().items():
            element = ET.SubElement(self.xml_title, keys) # The keys are the subelements in the XML file
            element.text = str(values) # Assign the content of each subelement

        '''Ignore this line, it sets up the XML file to be accepted'''
        self.file_tree = ET.tostring(self.xml_title, encoding='utf-8', xml_declaration=False)
        self.file_tree_domain = minidom.parseString(self.file_tree)
        '''Set indentation for better readability'''
        self.weather_report = self.file_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.weather_report = '\n'.join(line for line in self.weather_report.split('\n') if line.strip())

        '''Save the weather information to an XML file'''
        with open('weather_report.xml', 'w') as report_xml:
            report_xml.write(self.weather_report)
    
    def xml_speech(self):
        self.xml_data() # Call the xml_data() method

        self.weather_Condition = ET.fromstring(self.file_tree)
        weather_mp3 = '' # Empty string

        '''Loop through each element in the XML file and add it to the weather_mp3 variable'''
        for element in self.weather_Condition.iter():
            if element.text is not None: # Check for Not None to skip the root
                weather_mp3 += '{}, {}, \n'.format(element.tag, element.text)

        '''Save the mp3 file'''
        speech_mp3 = gTTS(text=weather_mp3, lang='en')
        speech_mp3.save('weather.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('weather.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

class WeatherAlert:
    def __init__(self, file):
        self.file = file

    def alerts(self):
        with open(self.file, 'r') as raw_data:
            self.weather_alert = json.load(raw_data)

        if 'alerts' in self.weather_alert:
            alert_information = {
                "Alert_Kind": self.weather_alert['alerts']['alert'][0]['event'],
                'Covered_Area': self.weather_alert['alerts']['alert'][0]['areas'],
                "Severeness": self.weather_alert['alerts']['alert'][0]['severity'],
                "Alert_Details": self.weather_alert['alerts']['alert'][0]['desc'],
                "Instruction": self.weather_alert['alerts']['alert'][0]['instruction']
            }
            return alert_information

    def alert_data(self): 
        #Weather_Data as root of the XML file
        self.xml_alert_title = ET.Element('Weather,Data')

        if self.alerts() is not None:
            for keys, values in self.alerts().items():
                alert = ET.SubElement(self.xml_alert_title, keys) # The keys are the subelements in the XML file
                alert.text = str(values) # Assign the content of each subelement

        '''Ignore this line, it sets up the XML file to be accepted'''
        self.alert_tree = ET.tostring(self.xml_alert_title, encoding='utf-8', xml_declaration=False)
        self.alert_tree_domain = minidom.parseString(self.alert_tree)
        '''Set indentation for better readability'''
        self.alert_report = self.alert_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.alert_report = '\n'.join(line for line in self.alert_report.split('\n') if line.strip())

        '''Save the weather information to an XML file'''
        with open('weather_alert.xml', 'w') as alert_xml:
            alert_xml.write(self.alert_report)
    
    def alert_speech(self):
        self.alert_data() # Call the alert_data() method

        self.alert_Condition = ET.fromstring(self.alert_tree)
        weather_alert_mp3 = '' # Empty string

        '''Loop through each element in the XML file and add it to the weather_alert_mp3 variable'''
        for alert in self.alert_Condition.iter():
            if alert.text is not None: # Check for Not None to skip the root
                weather_alert_mp3 += '{}, {}, \n'.format(alert.tag, alert.text)

        '''Save the mp3 file'''
        speech_mp3 = gTTS(text=weather_alert_mp3, lang='en')
        speech_mp3.save('alert.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('alert.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

class TimeCheck:
    def __init__(self):
        self.cur_time()

    def cur_time(self):
        time = str(datetime.datetime.now().strftime("Today is %B %d %Y. The time is %I:%M %p"))
        time_mp3 = gTTS(text=time, lang='en')
        time_mp3.save('time.mp3')
        os.system('time.mp3')

def wait_until_next_interval():
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    # Calculate the remaining time until the next 30-minute interval
    minutes_remaining = 30 - ((minutes + 1) % 30)
    seconds_remaining = 60 - seconds

    # Check if the current time is close to the next hour boundary
    if minutes_remaining == 0 and seconds_remaining < 60:
        minutes_remaining = 30

    # Convert the remaining time to seconds
    total_seconds = (minutes_remaining * 60) + seconds_remaining

    # Wait until the next interval
    time.sleep(total_seconds)


# Adi an mga Class Objects
weather_report = Weather('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
alert_report = WeatherAlert('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\practice_Class\\alerts.json')
current_time = TimeCheck()

# GPIO pin numbers
GPIO_D0 = 5
GPIO_D1 = 6
GPIO_D2 = 13
GPIO_D3 = 19
GPIO_StQ = 26

# GPIO setup
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# Button debounce time (in seconds)
DEBOUNCE_TIME = 0.2

# Set up GPIO pins
GPIO.setup(GPIO_D0, GPIO.IN)
GPIO.setup(GPIO_D1, GPIO.IN)
GPIO.setup(GPIO_D2, GPIO.IN)
GPIO.setup(GPIO_D3, GPIO.IN)
GPIO.setup(GPIO_StQ, GPIO.IN)


def button_pressed(channel):
    # Add your button press logic here
    key_tone_received = GPIO.input(GPIO_D0) + (GPIO.input(GPIO_D1) * 2) + (GPIO.input(GPIO_D2) * 4) + (GPIO.input(GPIO_D3) * 8)
    
    if key_tone_received == 1:
        weather_report.xml_speech()  # Play weather forecast
    elif key_tone_received == 2:
        current_time.cur_time()  # Display current time


# Add event detection for StQ pin
GPIO.add_event_detect(GPIO_StQ, GPIO.RISING, callback=button_pressed, bouncetime=int(DEBOUNCE_TIME * 1000))

# Add a try-finally block for proper GPIO cleanup
try:
    while True:
        # Your main code logic here

        if alert_report.alerts() is not None:
            alert_report.alert_speech()
        else:
            wait_until_next_interval()
            weather_report.xml_speech()

        wait_until_next_interval()
        weather_report.xml_speech()

finally:
    GPIO.cleanup()
