from discord.ext import commands
from pprint import pprint
import yaml

class RachmaninoffBot(commands.Bot):
    def add_cog(self, cog):
        with open('rachmaninoff_bot.yml') as bot_settings:
            settings = (yaml.load(bot_settings, Loader=yaml.FullLoader))
            
        if settings['debug']:
            pprint("- Adding cog " + type(cog).__name__)

        cog.load_settings(settings)
        super().add_cog(cog)

    def run(self, token):
        pprint("Starting rachmaninoff bot.")
        super().run(token)