from rachmaninoff.rachmaninoff_interface import RachmaninoffInterface
from discord.ext import commands
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime

class RachmaninoffTrafficCog(RachmaninoffInterface):

    def get_logs_collection(self):
        client = MongoClient(self.mongodb_connection)
        return client.rachmaninoff.trafficlogs

    @commands.command()
    async def log(self, ctx, name: str, day: str, date: str=''):
        if not self.is_allowed(ctx.author.name):
            return

        logs_collection = self.get_logs_collection()

        if date == '':
            submission_date = datetime.now()
        else:
            submission_date = datetime.strptime(date, '%m/%d/%y')

        log_json = {
            'name': name,
            'day': day,
            'date': submission_date,
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
        