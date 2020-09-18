from pprint import pprint
from discord.ext import commands

class InterfaceCog(commands.Cog):
    def __init__(self, bot, allowed_users, mongodb_connection=""):
        super().__init__()
        self.bot = bot
        self.allowed_users = allowed_users
        self.mongodb_connection = mongodb_connection
        self.debug = False

    def is_allowed(self, username):
        return username in self.allowed_users

    def log_action(self, message):
        if self.debug:
            pprint("RB LOG --- " + message)
        # TODO: Add code to log to file if debug is flagged or something

    def load_settings(self, settings):
        self.debug = settings['debug']
        self.default_zipcode = settings['default_zipcode']