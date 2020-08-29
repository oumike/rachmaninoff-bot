from discord.ext import commands

class RachmaninoffGeneralCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print('General: ' + message.content)

    @commands.command()
    async def test(self, ctx):
        await ctx.send('yes')

class RachmaninoffTrafficCog(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        print('Traffic: ' + message.content)

