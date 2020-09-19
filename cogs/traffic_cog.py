from cogs.interface_cog import InterfaceCog
from discord.ext import commands
from pprint import pprint
from pymongo import MongoClient
from datetime import datetime
import discord

class TrafficCog(InterfaceCog):

    def get_logs_collection(self):
        client = MongoClient(self.mongodb_connection)
        return client.rachmaninoff.trafficlogs

    @commands.command(hidden=True)
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

    @commands.command(hidden=True)
    async def getlogs(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        logs_collection = self.get_logs_collection()

        log_results = ''
        for log in logs_collection.find():
            date = log['date']
            log_results = log_results + 'name: ' + log['name'] + ', day: ' + log['day'] + ', date: ' + date.__format__('%m/%d/%Y') + '\n'
        
        logs_embed = discord.Embed()
        logs_embed.add_field(name='Traffic Logs', value=log_results)

        await ctx.send(embed=logs_embed)

    @commands.command(hidden=True)
    async def deletelogs(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        self.get_logs_collection().delete_many({})

        await ctx.send('Deleted all logs.')
        self.log_action('Deleted all logs.')
        