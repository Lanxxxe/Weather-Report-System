from lxml import etree
import requests, json, os, time
from gtts import gTTS
from time import sleep
from datetime import datetime 
import threading, pygame
import schedule, datetime

''''
Tacloban City
Temperature: 69 degrees
Chance of rain: 69%
Humidity: 69%
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
            "Location" : self.weather_response['location']['name'],
            "Temperature" : '{} degrees'.format(self.weather_response['current']['temp_c']),
            "Humidity" : '{} percent'.format(self.weather_response['current']['humidity']),
            "Precipitation" : '{} percent'.format(self.weather_response['forecast']['forecastday'][0]['day']['daily_chance_of_rain'])

        }   
        return self.weather_information

    def xml_speech(self): 
        #Weather_Data an root ng xml file

        xml_title = etree.Element('WeatherData')

        for keys, values in self.weather_data().items():
            element = etree.SubElement(xml_title, str(keys)) #Yung keys po ung mga subelement sa xml file
            element.text = str(values) # tapos adi an content ng bawat subelemet

        '''Don't mind this line, gin seset la ini para tanggapin sa xml file'''
        file_tree = etree.tostring(xml_title, encoding='utf-8', pretty_print=True)
        '''Adi nag seset ng indention para maayos tingnan'''

        '''Tapos adi ginsasave ha xml file an mga weather information'''
        with open('weather_report.xml', 'w') as report_xml:
            report_xml.write(file_tree.decode())

        while True:
            weather_mp3 = '' #Empty String la ini

            '''loop adi para ipasok sa ung bawat laman ng xml file into the weather_mp3 variable'''
            for element in xml_title.getiterator(): 
                if element.text is not None: #nag condition po ako ng Not None para ma skip an root
                    weather_mp3 += '{}, {}, \n'.format(element.tag, element.text) 

            '''gin Save la an mp3'''
            speech_mp3 = gTTS(text=weather_mp3, lang='en')
            speech_mp3.save('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')  
            pygame.mixer.init()
            pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                continue

weather_report = weather('Tacloban City', 'cc411f08a7b9463fbb2131058232406')

def calculate_next_interval():
    now = datetime.datetime.now()
    minutes = now.minute

    next_interval = datetime.datetime(now.year, now.month, now.day, now.hour, minutes + 5 - (minutes % 5))

    return next_interval

def wait_until_next_interval():
    next_interval = calculate_next_interval()
    time_difference = (next_interval - datetime.datetime.now()).total_seconds()

    if time_difference > 0:
        time.sleep(time_difference)

# Schedule the program to run every 5 minutes
schedule.every(5).minutes.do(weather_report.xml_speech)
#Adi an mga Class Objects

if __name__ == "__main__":
    def interval_report():
        wait_until_next_interval()
        report = weather_report.xml_speech()
        while True:
            schedule.run_pending()
            time.sleep(1)   

    weatherReport = threading.Thread(target=interval_report)
    weatherReport.start()

    while True:
        user = input()
        if user == "":
            weather_report.xml_speech()

