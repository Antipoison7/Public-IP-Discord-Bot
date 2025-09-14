import requests
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!",intents=intents)

@bot.event
async def on_ready():
    print('Started the bot')
    check_ip_changed.start()

@bot.command()
async def feed(ctx):
    await ctx.send("Why are you trying to feed me, I'm a DNS server")
    

@bot.command()
async def unfeed(ctx):
    await ctx.send("Bruh")

@bot.command()
async def set_notifs(ctx):
    channel_id = ctx.channel.id
    with open("notifs_channel.txt", "w") as file:
        file.write(str(channel_id))
        await ctx.send(f"The IP notifications has been set to channel: {str(channel_id)}")

@bot.command()
async def public(ctx):
    try:
        response = requests.get("https://ipinfo.io/ip", timeout=10)

        ip_string = response.content.decode('utf-8')

        if response.status_code == 404:
            await ctx.send("404 Error, I didn't even know this could happen")
        else:
            await ctx.send(f"Public IP: `{ip_string}`")

    except requests.Timeout:
        await ctx.send("Request Timed Out")

@tasks.loop(minutes=10.0)
async def check_ip_changed():
    try:
        if os.path.exists("notifs_channel.txt"):
            with open("notifs_channel.txt", "r") as file:
                channel_id = int(file.readline())

            prev_ip = "0"
            if os.path.exists("prev_ip.txt"):
                with open("prev_ip.txt", "r") as file:
                    prev_ip = file.readline()

            channel = bot.get_channel(channel_id)

            response = requests.get("https://ipinfo.io/ip", timeout=10)

            ip_string = response.content.decode('utf-8')


            if response.status_code != 404:
                with open("prev_ip.txt", "w") as file:
                    file.write(str(ip_string))

            if response.status_code == 404:
                await channel.send("404 Error, I didn't even know this could happen")
            else:
                if ip_string != prev_ip:
                    await channel.send(f"IP Has Changed: `{ip_string}`")

    except requests.Timeout:
        await channel.send("Request Timed Out")


bot.run(api_key)
