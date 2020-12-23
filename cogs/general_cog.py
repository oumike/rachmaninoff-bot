from cogs.interface_cog import InterfaceCog
from pprint import pprint
from uptime import boottime
from speedtest import Speedtest
from discord.ext import commands
import discord
import requests, json
import random
import re
from lxml import html

class GeneralCog(InterfaceCog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == 'Rachmaninoffs Bot':
            return

        self.log_action(message.author.name + ': ' + message.content)

    @commands.command(name='boottime', aliases=['bt'], help='Shows boottime of server where bot is hosted.')
    async def boottime(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        boot_info = boottime()
        await ctx.send(boot_info.isoformat())

    @commands.command(name='speedtest', aliases=['st'], help='Runs speedtest on server where bot is hosted.')
    async def speedtest(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        pprint('Running speedtest...')
        s = Speedtest()
        s.get_servers(servers=[])
        s.get_best_server()
        s.download(threads=None)
        s.upload(threads=None)
        s.results.share()
        
        speedtest_results = s.results.dict()
        download_in_mb = speedtest_results['download']/(1000*1000)
        upload_in_mb = speedtest_results['upload']/(1000*1000)

        print('Finished running speedtest.')

        share = str(speedtest_results['share'])

        speedtest_results = "Download: {0}\nUpload: {1}\nShare URL: {2}"
        speedtest_results = speedtest_results.format(str(round(download_in_mb, 2)),
                                                        str(round(upload_in_mb, 2)), 
                                                        str(share))

        speedtest_embed = discord.Embed()
        speedtest_embed.add_field(name="Speedtest Results", value=speedtest_results)

        await ctx.send(embed=speedtest_embed)

    @commands.command(name='catfact', aliases=['cf'], help='Random cat fact.')
    async def catfact(self, ctx):
        url = 'https://cat-fact.herokuapp.com/facts' 
        response = requests.get(url) 
        cat_facts = response.json()

        random_cat_fact = random.choice(cat_facts['all'])
        catfact = random_cat_fact['text'] + "\nBy " + random_cat_fact['user']['name']['first'] + " " + random_cat_fact['user']['name']['last']

        catfact_embed = discord.Embed()
        catfact_embed.add_field(name="Random Cat Fact", value=catfact)
        await ctx.send(embed=catfact_embed)

    @commands.command(name='numberfact', aliases=['nf'], help='Random number fact')
    async def numberfact(self, ctx):
        url = 'http://numbersapi.com/random/trivia'
        numberfact = requests.get(url)
 
        numberfact_embed = discord.Embed()
        numberfact_embed.add_field(name='Number Fact', value=numberfact.text)
        await ctx.send(embed=numberfact_embed)

    @commands.command(hidden=True)
    async def test(self, ctx):
        for command in self.bot.commands:
            pprint(command.name)

    @commands.command(name='fml', help='Random FML')
    async def fml(self, ctx):
        remove_newline_reg = re.compile('\n')
        author_reg = re.compile('By (.*?)')

        response = requests.get('https://www.fmylife.com/random')

        html_tree = html.fromstring(response.content)
        text = html_tree.xpath('.//div[2]/a/text()')[0]
        
        author_line = None
        for line in html_tree.xpath('.//div[1]/text()'):
            line = line.strip()
            line = remove_newline_reg.sub(' ', line)
            if author_reg.search(line):
                author_line = line
                break

        await ctx.send(text + '\n' + author_line)

