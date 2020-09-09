from rachmaninoff.rachmaninoff_interface import RachmaninoffInterface
from discord.ext import commands

class RachmaninoffWeatherCog(RachmaninoffInterface):
    def __init__(self, bot, allowed_users, openweathermap_apikey, mongodb_connection=''):
        self.openweathermap_apikey = openweathermap_apikey
        super().__init__(bot, allowed_users, mongodb_connection=mongodb_connection)
