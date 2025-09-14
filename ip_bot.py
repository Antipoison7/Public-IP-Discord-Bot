import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.command()
async def feed(ctx):
    await ctx.send("Why are you trying to feed me, I'm a DNS server")
    

@bot.command()
async def unfeed(ctx):
    await ctx.send("Bruh")


bot.run(api_key)
