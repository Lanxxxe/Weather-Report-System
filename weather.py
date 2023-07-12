import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests, json, os, time
import RPi.GPIO as g
import pygame
import datetime
from gtts import gTTS
from time import sleep
''''
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

class weather: 
    '''Initializing'''
    def __init__(self, api_location, api_key):
        self.location = api_location
        self.key = api_key
        self.accuweather_url = requests.get('http://api.weatherapi.com/v1/forecast.json?key={}&q={}&days=1&aqi=yes&alerts=yes'.format(self.key, self.location))
        self.accuweather_url.raise_for_status
        self.weather_response = json.loads(self.accuweather_url.text)
    
    def weather_data(self):
        '''Getting some information on WeatherAPI as Dicktionary'''
        self.weather_information = {
            "Today-is": str(datetime.datetime.now().strftime("%B %d %Y. The time is %I:%M %p")),
            "Weather-Report-in" : self.weather_response['location']['name'],
            "Temperature" : '{} degrees'.format(self.weather_response['current']['temp_c']),
            "Humidity" : '{} percent'.format(self.weather_response['current']['humidity']),
            "Chance-Of-Rain" : '{} percent'.format(self.weather_response['forecast']['forecastday'][0]['day']['daily_chance_of_rain'])
        }   
        return self.weather_information

    def xml_data(self): 
        #Weather_Data an root ng xml file
        self.xml_title = ET.Element('Weather_Data')

        for keys, values in self.weather_data().items():
            element = ET.SubElement(self.xml_title, keys) #Yung keys po ung mga subelement sa xml file
            element.text = str(values) # tapos adi an content ng bawat subelemet

        '''Don't mind this line, gin seset la ini para tanggapin sa xml file'''
        self.file_tree = ET.tostring(self.xml_title, encoding='utf-8', xml_declaration=False)
        self.file_tree_domain = minidom.parseString(self.file_tree)
        '''Adi nag seset ng indention para maayos tingnan'''
        self.weather_report = self.file_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.weather_report = '\n'.join(line for line in self.weather_report.split('\n') if line.strip())

        '''Tapos adi ginsasave ha xml file an mga weather information'''
        with open('weather_report.xml', 'w') as report_xml:
            report_xml.write(self.weather_report)
    
    def xml_speech(self):
        self.xml_data() #gin call la an xml_data() method


        self.weather_Condition = ET.fromstring(self.file_tree)
        weather_mp3 = '' #Empty String la ini

        '''loop adi para ipasok sa ung bawat laman ng xml file into the weather_mp3 variable'''
        for element in self.weather_Condition.iter(): 
            if element.text is not None: #nag condition po ako ng Not None para ma skip an root
                weather_mp3 += '{}, {}, \n'.format(element.tag, element.text) 

        '''gin Save la an mp3'''
        speech_mp3 = gTTS(text=weather_mp3, lang='en')
        speech_mp3.save('weather.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

class weather_alert:
    def __init__(self, file):
        self.file = file

    def alerts(self):
        with open(self.file, 'r') as rawData:
            self.weather_alert = json.load(rawData)

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
        #Weather_Data an root ng xml file
        self.xmlalert_title = ET.Element('Weather,Data')

        if self.alerts() is not None:
            for keys, values in self.alerts().items():
                alert = ET.SubElement(self.xmlalert_title, keys) #Yung keys po ung mga subelement sa xml file
                alert.text = str(values) # tapos adi an content ng bawat subelemet

        '''Don't mind this line, gin seset la ini para tanggapin sa xml file'''
        self.alert_tree = ET.tostring(self.xmlalert_title, encoding='utf-8', xml_declaration=False)
        self.alert_tree_domain = minidom.parseString(self.alert_tree)
        '''Adi nag seset ng indention para maayos tingnan'''
        self.alert_report = self.alert_tree_domain.toprettyxml(indent='\t', newl='\n')
        self.alert_report = '\n'.join(line for line in self.alert_report.split('\n') if line.strip())

        '''Tapos adi ginsasave ha xml file an mga weather information'''
        with open('weather_alert.xml', 'w') as alert_xml:
            alert_xml.write(self.alert_report)
    
    def alert_speech(self):
        self.alert_data() #gin call la an xml_data() method

        self.alert_Condition = ET.fromstring(self.alert_tree)
        weather_alert_mp3 = '' #Empty String la ini

        '''loop adi para ipasok sa ung bawat laman ng xml file into the weather_mp3 variable'''
        for alert in self.alert_Condition.iter(): 
            if alert.text is not None: #nag condition po ako ng Not None para ma skip an root
                weather_alert_mp3 += '{}, {}, \n'.format(alert.tag, alert.text) 

        '''gin Save la an mp3'''
        speech_mp3 = gTTS(text=weather_alert_mp3, lang='en')
        speech_mp3.save('alert.mp3')
        pygame.mixer.init()
        pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\alert.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue

class time_check:
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

#Adi an mga Class Objects
weather_report = weather('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
alert_report = weather_alert('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\practice_Class\\alerts.json')
current_time = time_check()
        
if __name__ == "__main__":
    '''Adi an tikang sa dtmf.py'''
    GPIO_D0  = 5
    GPIO_D1  = 6
    GPIO_D2  = 13
    GPIO_D3  = 19
    GPIO_StQ = 26   
    
    g.setmode(g.BCM)
    g.setwarnings(False)

    #infinite po magrurun ung program once na ma run an file
    while True:

        sleep(0.1) # standaard warde is 0.1 sec
        g.setup(GPIO_D0, g.IN)
        g.setup(GPIO_D1, g.IN)
        g.setup(GPIO_D2, g.IN)
        g.setup(GPIO_D3, g.IN)
        g.setup(GPIO_StQ, g.IN)

        D0 = g.input(GPIO_D0)
        D1 = g.input(GPIO_D1)
        D2 = g.input(GPIO_D2)
        D3 = g.input(GPIO_D3)
        StQ= g.input(GPIO_StQ)
        
        if StQ == True:
            # Check for DTMF tone input
            key_tone_received = D0+(D1*2)+(D2*4)+(D3*8)

            if key_tone_received ==10:
                key_tone_received=0
                '''adi an para ha input ng DTMF'''
                if key_tone_received == 1:
                    weather_report.xml_speech() #if 1 an pinindot, magrurun an weather forecast
                if key_tone_received == 2:
                    current_time.cur_time() #if 2 namn po an pinindot, gagana an time check. Time lang po yan di kasama ung month and day


        else:
            while True:
                if alert_report.alerts() is not None:
                    alert_report.alert_speech()
                else:
                    wait_until_next_interval()
                    weather_report.xml_speech()

                wait_until_next_interval()
                weather_report.xml_speech()

