from discord.ext import commands
from pprint import pprint


class RachmaninoffBot(commands.Bot):
    def add_cog(self, cog):
        pprint("- Adding cog " + type(cog).__name__)
        super().add_cog(cog)

    def run(self, token):
        pprint("Starting rachmaninoff bot.")
        super().run(token)