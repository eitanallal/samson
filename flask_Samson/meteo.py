import requests
import json
from datetime import datetime, timedelta

class Weather:
    def __init__(self):
        self.params = {
            'latitude': '30.0',
            'longitude': '35.0',
            'start_date': '2023-01-01',
            'start_time': '05:00',
            'end_date': '2023-01-01',
            'hourly': 'temperature_2m',
        }

    def get_weather(self):
        response = requests.get('https://archive-api.open-meteo.com/v1/era5', params=self.params)

        if response.status_code == 200:
            data = json.loads(response.text)

            hourly_data = data['hourly']['temperature_2m']

            hourly_time = data['hourly']['time']
            
            print(hourly_data)
            print(hourly_time)
            
            ##TODO: Need to add humidity (different contact between the wheels and the runway)
            ##TODO: Need to add wind (different Take off speed)

        else:
            print(f"Erreur lors de la requête à l'API. Code de statut : {response.status_code}")
            
    def set_longitude(self, longitude):
        self.params['longitude']=longitude
        
    def set_latitude(self, latitude): #lattitude
        self.params['latitude']=latitude
        
    def set_date(self, date): #date
        input_date = datetime.strptime(date, "%Y-%m-%d")
        next_date = input_date + timedelta(days=1)
        next_date_string = next_date.strftime("%Y-%m-%d")
        self.params['start_date']=date
        self.params['end_date']=next_date_string
        
        
    def set_time(self, time): #time
        self.params['time']=time

weather = Weather()

weather.set_longitude(50)
weather.set_latitude(-5)
weather.set_date("2023-01-10")
print(weather.params)

weather.get_weather()