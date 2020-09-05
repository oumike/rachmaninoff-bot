from discord.ext import commands
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime # Current date time in local system print(datetime.now())
import speedtest

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

class RachmaninoffGeneralCog(RachmaninoffInterface):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == 'Rachmaninoffs Bot':
            return

        self.log_action(message.author.name + ': ' + message.content)

    @commands.command()
    async def speedtest(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        pprint('Running speedtest...')
        s = speedtest.Speedtest()
        s.get_servers(servers=[])
        s.get_best_server()
        s.download(threads=None)
        s.upload(threads=None)
        s.results.share()
        
        speedtest_results = s.results.dict()
        download_in_mb = speedtest_results['download']/(1000*1000)
        upload_in_mb = speedtest_results['upload']/(1000*1000)

        print('finished running speedtest.')

        await ctx.send('Download (megabits): ' + str(round(download_in_mb, 2)))
        await ctx.send('Upload (megabits): ' + str(round(upload_in_mb, 2)))
        await ctx.send('Share URL: ' + str(speedtest_results['share']))


    @commands.command()
    async def test(self, ctx):
        await ctx.send('yes')

class RachmaninoffTrafficCog(RachmaninoffInterface):

    def get_logs_collection(self):
        client = MongoClient(self.mongodb_connection)
        return client.trafficlogs.logs

    @commands.command()
    async def log(self, ctx, name: str, day: str, date: str):
        if not self.is_allowed(ctx.author.name):
            return

        logs_collection = self.get_logs_collection()

        log_json = {
            'name': name,
            'day': day,
            'date': datetime.strptime(date, '%m/%d/%y'),
            'created_at': datetime.now()
        }

        logs_collection.insert_one(log_json)

        await ctx.send('Log created.')
        self.log_action('Log created.')

    @commands.command()
    async def getlogs(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        logs_collection = self.get_logs_collection()

        for log in logs_collection.find():
            date = log['date']
            await ctx.send('name: ' + log['name'] + ', day: ' + log['day'] + ', date: ' + date.__format__('%m/%d/%Y'))
        
    @commands.command()
    async def deletelogs(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        self.get_logs_collection().delete_many({})

        await ctx.send('Deleted all logs.')
        self.log_action('Deleted all logs.')
        