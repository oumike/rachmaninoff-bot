from cogs.interface_cog import InterfaceCog
from discord.ext import commands
import discord
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
    async def w(self, ctx, zip=''):
        return await self.weather(ctx, zip)

    @commands.command()
    async def weather(self, ctx, zipcode=''):
        weather_mongo_collection= self.get_weather_collection()

        if zipcode == '':
            weather_document = weather_mongo_collection.find_one({'name': 'last_zip_used', 'user': ctx.author.name})
            if weather_document:
                zipcode = weather_document['value']
            else:
                zipcode = self.default_zipcode
        
        weather_mongo_collection.update_one({'name':'last_zip_used', 'user':ctx.author.name}, 
                                                {'$set': {'value': zipcode}},
                                                upsert=True)
            
        url = self.openweathermap_base_url + 'appid=' + self.openweathermap_apikey + '&zip=' + str(zipcode) 

        response = requests.get(url) 
        weather_data = response.json()

        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        feels_like = round(self.convert_to_fahrenheit(feels_like))
        wind = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        weather_embed = discord.Embed(title="")

        answer_string = 'Currently {1}\nFeels like {2}F\nWind is {3}mph\nHumidity at {4}%'
        answer_string = answer_string.format(city, description, feels_like, wind, humidity)
        
        weather_embed.add_field(name=city, value=answer_string)
        await ctx.send(embed=weather_embed)

        # await ctx.send(answer_string)
