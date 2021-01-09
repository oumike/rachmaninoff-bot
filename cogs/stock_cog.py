from cogs.interface_cog import InterfaceCog
from discord.ext import commands
from pprint import pprint
from datetime import datetime
import discord
import requests, json
import yfinance as yf

class StockCog(InterfaceCog):

    def build_embed(self, json_input, name):
        embed = discord.Embed()

        stock_text = f"""
Ask: {str(json_input["ask"])}
Day Low/High: {str(json_input["dayLow"])} / {str(json_input["dayHigh"])}            
Previous Closing Price: {str(json_input["previousClose"])}
Two Hundred Day Average: {str(json_input["twoHundredDayAverage"])}
52 Week Low/High: {str(json_input["fiftyTwoWeekLow"])} / {str(json_input["fiftyTwoWeekHigh"])}
        """

        embed.add_field(name=name, value=stock_text)

        return embed


    @commands.command(name="stock", aliases=['s'], help="Current stock information")
    async def get_stock_information(self, ctx, stock_symbol: str):
        if not self.is_allowed(ctx.author.name):
            return

        s = yf.Ticker(stock_symbol)

        await ctx.send(embed=self.build_embed(s.info, 'Company Name: ' + s.info['shortName']))