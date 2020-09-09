from pprint import pprint
from discord.ext import commands

class RachmaninoffInterface(commands.Cog):
    def __init__(self, bot, allowed_users, mongodb_connection=""):
        super().__init__()
        self.bot = bot
        self.allowed_users = allowed_users
        self.mongodb_connection = mongodb_connection

    def is_allowed(self, username):
        return username in self.allowed_users

    def log_action(self, message):
        pprint("RB LOG --- " + message)
        # TODO: Add code to log to file if debug is flagged or something