import xml.dom.minidom as minidom
import xml.etree.ElementTree as ET
import requests, json, os, time
import datetime
import pygame
from gtts import gTTS
from time import sleep


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
        speech_mp3.save('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
        print("Time Played: " + str(datetime.datetime.now().strftime("%I:%M %p")))
        pygame.mixer.init()
        pygame.mixer.music.load('C:\\Users\\Student\\OneDrive\\Desktop\\Rico_Parena\\weather.mp3')
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        
        sleep(2 * 60)
        os.remove('weather.mp3')
    

def wait_until_next_interval():
    now = datetime.datetime.now()
    minutes = now.minute
    seconds = now.second

    # Calculate the remaining time until the next 30-minute interval
    minutes_remaining = 5 - ((minutes + 1)% 5)
    seconds_remaining = 60 - seconds

    # Check if the current time is close to the next hour boundary
    if minutes_remaining == 0 and seconds_remaining < 60:
        minutes_remaining = 5

    # Convert the remaining time to seconds
    total_seconds = (minutes_remaining * 60) + seconds_remaining

    # Wait until the next interval
    time.sleep(total_seconds)

weather_report = weather('Tacloban City', 'cc411f08a7b9463fbb2131058232406')
# Schedule the program to run every 5 minutes

if __name__ == "__main__":
    # Calculate and wait until the next interval
    print("Time being runned: " + str(datetime.datetime.now().strftime("%I:%M %p")))

    # Continuously run the schedule
    while True:
        wait_until_next_interval()
        weather_report.xml_speech()
