from rachmaninoff.rachmaninoff_interface import RachmaninoffInterface
from discord.ext import commands
from pprint import pprint
import requests, json

class RachmaninoffWeatherCog(RachmaninoffInterface):
    def __init__(self, bot, allowed_users, openweathermap_apikey, mongodb_connection=''):
        self.openweathermap_apikey = openweathermap_apikey
        self.openweathermap_base_url = "http://api.openweathermap.org/data/2.5/weather?"
        super().__init__(bot, allowed_users, mongodb_connection=mongodb_connection)

    def convert_to_fahrenheit(self, kelvin):
        return (kelvin - 273.15) * 9/5 + 32

    @commands.command()
    async def weather(self, ctx, zip):
        if not self.is_allowed(ctx.author.name):
            return

        url = self.openweathermap_base_url + 'appid=' + self.openweathermap_apikey + '&zip=' + zip 
        pprint('Weather url: ' + url)

        response = requests.get(url) 
        weather_data = response.json()
        pprint(weather_data)

        city = weather_data['name']
        description = weather_data['weather'][0]['description']
        feels_like = weather_data['main']['feels_like']
        feels_like = round(self.convert_to_fahrenheit(feels_like))
        wind = weather_data['wind']['speed']
        humidity = weather_data['main']['humidity']

        answer_string = 'Weather for {0}: {1}, Feels like: {2}F, Wind: {3}mph, Humidity: {4}%'
        answer_string = answer_string.format(city, description, feels_like, wind, humidity)
        
        await ctx.send(answer_string)

# Weather for Farmington Hills, MI, US: 🌥 broken clouds 60°F (15°C) Feels like: 59°F (15°C) Wind: 8mph ↑↗ Humidity: 97%