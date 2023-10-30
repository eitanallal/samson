import requests
import json
import numpy as np
import pandas as pd

'''
current/forecast: 'https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m'
'''
class Weather:
    '''
    Class made by Eitan
    '''
    def __init__(self):
        self.params = {
            'latitude': '52.52',
            'longitude': '13.41',
            'hourly': 'temperature_2m,relativehumidity_2m,windspeed_10m,winddirection_10m,pressure_msl,precipitation_probability,is_day',
            'start_date':'2023-01-01',
            'end_date': '2023-01-01'
        }

        
    def get_weather(self):
        # print('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m'))
        command = "https://api.open-meteo.com/v1/forecast"
        print("Requested weather forcast with parameters:", self.params)
        response = requests.get(command, params=self.params)

        if response.status_code == 200:
            data = json.loads(response.text)
            temperature = np.array(data['hourly']['temperature_2m'])
            humidity = np.array(data['hourly']['relativehumidity_2m'])
            windspeed = np.array(data['hourly']['windspeed_10m'])
            winddirection_10m = np.array(data['hourly']['winddirection_10m'])
            pressure_msl = np.array(data['hourly']['pressure_msl'])
            is_day = np.array(data['hourly']['is_day'])
            precipitation = np.array(data['hourly']['precipitation_probability'])
            time = np.array(data['hourly']['time'])
            
            time_only = np.array([s.split('T')[1] for s in time])
            date_only = np.array([s.split('T')[0] for s in time])
            data_table = {'date':date_only,
                          'time': time_only,
                          'temperature': temperature,
                          'humidity': humidity,
                          'windspeed': windspeed,
                          'winddirection_10m': winddirection_10m,
                          'pressure_msl': pressure_msl,
                          'precipitation': precipitation,
                          'is_day': is_day}
            
            df = pd.DataFrame(data_table)
            
            self.df = df
                        
            ##TODO: Need to add humidity (different contact between the wheels and the runway)
            ##TODO: Need to add wind (different Take off speed)
            return df

        else:
            print(f"Error in the API request. Status code: {response.status_code}")
            return None
            
    def set_longitude(self, longitude):
        self.params['longitude']=longitude
        
    def set_latitude(self, latitude):
        self.params['latitude']=latitude
        
    def set_date_start(self, date):
        self.params['start_date']=date        
        
    def set_date_end(self, date):
        self.params['end_date']=date
        
    def set_all_params(self, longitude, latitude, date_start, date_end):
        self.set_longitude(longitude)
        self.set_latitude(latitude)
        self.set_date_start(date_start)
        self.set_date_end(date_end)
        
    def get_weather_output(self):
        return self.df
    
    def get_current_temperature(self):
        # print('https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&current=temperature_2m,windspeed_10m&hourly=temperature_2m,relativehumidity_2m,windspeed_10m'))
        command = "https://api.open-meteo.com/v1/forecast"
        params = {
            'latitude': '30.0',
            'longitude': '35.0',
            'current':'temperature_2m,windspeed_10m,winddirection_10m,pressure_msl,is_day'
        }
        response = requests.get(command, params=params)

        if response.status_code == 200:
            data = json.loads(response.text)
            temperature = data['current']['temperature_2m']
            # windspeed = data['current']['windspeed_10m']
            # winddirection_10m = data['current']['winddirection_10m']
            # pressure_msl = data['current']['pressure_msl']
            # is_day = data['current']['is_day']
            # time = data['current']['time']
            
            return temperature

        else:
            print(f"Error in the API request. Status code: {response.status_code}")
            return None
        
weather_forecast = Weather()
weather_forecast.get_current_temperature()        