from cogs.interface_cog import InterfaceCog
from pprint import pprint
from uptime import boottime
from speedtest import Speedtest
from discord.ext import commands
import discord

class GeneralCog(InterfaceCog):
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.name == 'Rachmaninoffs Bot':
            return

        self.log_action(message.author.name + ': ' + message.content)

    @commands.command()
    async def bt(self, ctx):
        return await self.boottime(ctx)

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

        print('Finished running speedtest.')

        share = str(speedtest_results['share'])

        speedtest_results = "Download: {0}\nUpload: {1}\nShare URL: {2}"
        speedtest_results = speedtest_results.format(str(round(download_in_mb, 2)),
                                                        str(round(upload_in_mb, 2)), 
                                                        str(share))

        speedtest_embed = discord.Embed()
        speedtest_embed.add_field(name="Speedtest Results", value=speedtest_results)

        await ctx.send(embed=speedtest_embed)


    @commands.command()
    async def test(self, ctx):
        await ctx.send('yes')
