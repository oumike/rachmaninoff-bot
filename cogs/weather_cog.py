from cogs.interface_cog import InterfaceCog
from discord.ext import commands
from pprint import pprint
import requests, json
from pymongo import MongoClient

class WeatherCog(InterfaceCog):
    def __init__(self, bot, allowed_users, openweathermap_apikey, mongodb_connection=''):
        self.openweathermap_apikey = openweathermap_apikey
        self.openweathermap_base_url = "http://api.openweathermap.org/data/2.5/weather?"
        super().__init__(bot, allowed_users, mongodb_connection=mongodb_connection)

    def convert_to_fahrenheit(self, kelvin):
        return (kelvin - 273.15) * 9/5 + 32

    def get_weather_collection(self):
        client = MongoClient(self.mongodb_connection)
        return client.rachmaninoff.weather

    @commands.command()
    async def weather(self, ctx, zip=''):
        weather_mongo_collection= self.get_weather_collection()

        if zip == '':
            weather_document = weather_mongo_collection.find_one({'name': 'last_zip', 'user': ctx.author.name})
            zip = weather_document['value']
        else:
            weather_mongo_collection.update_one({'name':'last_zip', 'user':ctx.author.name}, 
                                                    {'$set': {'value': zip}},
                                                    upsert=True)
            
        url = self.openweathermap_base_url + 'appid=' + self.openweathermap_apikey + '&zip=' + zip 
        pprint('Weather url: ' + url)

        response = requests.get(url) 
        weather_data = response.json()

        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        feels_like = round(self.convert_to_fahrenheit(feels_like))
        wind = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        answer_string = 'Weather for {0}: {1}, Feels like: {2}F, Wind: {3}mph, Humidity: {4}%'
        answer_string = answer_string.format(city, description, feels_like, wind, humidity)
        
        await ctx.send(answer_string)
