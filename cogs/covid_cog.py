from cogs.interface_cog import InterfaceCog
from discord.ext import commands
from pprint import pprint
from datetime import datetime
import discord
import requests, json


class CovidCog(InterfaceCog):

    def build_embed(self, json_input, name):
        embed = discord.Embed()
        covid_discord_text = f"""
        Positive: {str(json_input['positive'])}
Negative: {str(json_input['negative'])}
Hospitalized Currently: {str(json_input['hospitalizedCurrently'])}
Hospitalized Cumulative: {str(json_input['hospitalizedCumulative'])}
Recovered: {str(json_input['recovered'])}
Death: {str(json_input['death'])}
        """

        embed.add_field(name=name, value=covid_discord_text)

        return embed



    @commands.command(name="covid-state", help="Current Covid-19 Information by State")
    async def covidstate(self, ctx, state: str):
        url = "https://covidtracking.com/api/states"
        response = requests.request("GET", url, headers={}, data={})

        state_results = {}
        for state_json in response.json():
            if state_json['state'] == state.upper():
                state_results = state_json
                break

        await ctx.send(embed=self.build_embed(state_results, 'Current State: ' + state.upper()))

    @commands.command(name="covid-us", help="Current Covid-19 Information for the United States")
    async def covidus(self, ctx):
        url = "http://covidtracking.com/api/us"
        response = requests.request("GET", url, headers={}, data={})

        await ctx.send(embed=self.build_embed(response.json()[0], 'Current US'))