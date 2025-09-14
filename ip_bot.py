import requests
import discord
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("API_KEY")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="/", intents=intents)

@bot.event
async def on_ready():
    print('Started the bot')
    await bot.tree.sync()
    check_ip_changed.start()

@bot.tree.command(name="feed", description="Feed the bot")
async def feed(interaction: discord.Interaction):
    await interaction.response.send_message("Why are you trying to feed me, I'm a DNS server")
    

@bot.tree.command(name="unfeed", description="Unfeed the bot")
async def unfeed(interaction: discord.Interaction):
    await interaction.response.send_message("Bruh")

@bot.tree.command(name="set_notifs", description="Sets the channel that the automated change notifications are sent to")
async def set_notifs(interaction: discord.Interaction):
    channel_id = interaction.channel.id
    with open("notifs_channel.txt", "w") as file:
        file.write(str(channel_id))
        await interaction.response.send_message(f"The IP notifications has been set to channel: {str(channel_id)}")

@bot.tree.command(name="public_ip", description="Outputs the current public IP address")
async def public_ip(interaction: discord.Interaction):
    try:
        response = requests.get("https://ipinfo.io/ip", timeout=10)

        ip_string = response.content.decode('utf-8')

        if response.status_code == 404:
            await interaction.response.send_message("404 Error, I didn't even know this could happen")
        else:
            with open("prev_ip.txt", "w") as file:
                file.write(str(ip_string))
            
            await interaction.response.send_message(f"Public IP: `{ip_string}`")

    except requests.Timeout:
        await interaction.response.send_message("Request Timed Out")

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
