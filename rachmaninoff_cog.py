from discord.ext import commands
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime # Current date time in local system print(datetime.now())

class RachmaninoffInterface(commands.Cog):
    def __init__(self, bot, allowed_users, mongodb_connection):
        super().__init__()
        self.bot = bot
        self.allowed_users = allowed_users
        self.mongodb_connection = mongodb_connection

    def is_allowed(self, username):
        return username in self.allowed_users

class RachmaninoffGeneralCog(commands.Cog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == 'Rachmaninoffs Bot':
            return

        print(message.author.name + ':' + message.content)

    @commands.command()
    async def test(self, ctx):
        await ctx.send('yes')

class RachmaninoffTrafficCog(RachmaninoffInterface):
    @commands.command()
    async def log(self, ctx, name: str, day: str):
        if not self.is_allowed(ctx.author.name):
            return

        client = MongoClient(self.mongodb_connection)
        db = client.trafficlogs

        log_json = {
            'name': name,
            'day': day,
            'datetime': datetime.now()

        }

        db.logs.insert_one(log_json)

        await ctx.send('Log created!')
        print("Log created!")
        
    @commands.command()
    async def getlogs(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        client = MongoClient(self.mongodb_connection)
        db = client.trafficlogs

        for log in db.logs.find():
            await ctx.send('name: ' + log['name'] + ', day: ' + log['day'])
        
    @commands.command()
    async def deletelogs(self, ctx):
        if not self.is_allowed(ct.author.name):
            return

        client = MongoClient(self.mongodb_connection)
        db = client.trafficlogs

        for log in db.logs.find():
            log.delete()
        
        