from cogs.interface_cog import InterfaceCog
from pprint import pprint
from uptime import boottime
from speedtest import Speedtest
from discord.ext import commands

class GeneralCog(InterfaceCog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == 'Rachmaninoffs Bot':
            return

        self.log_action(message.author.name + ': ' + message.content)

    @commands.command()
    async def boottime(self, ctx):
        if not self.is_allowed(ctx.author.name):
            return

        boot_info = boottime()
        await ctx.send(boot_info.isoformat())

    @commands.command()
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

        print('finished running speedtest.')

        await ctx.send('Download (megabits): ' + str(round(download_in_mb, 2)))
        await ctx.send('Upload (megabits): ' + str(round(upload_in_mb, 2)))
        await ctx.send('Share URL: ' + str(speedtest_results['share']))


    @commands.command()
    async def test(self, ctx):
        await ctx.send('yes')
