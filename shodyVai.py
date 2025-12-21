# these are the modules we need to import
import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os

#load the dotenv file and get the token
load_dotenv()
token = os.getenv('TOKENS')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.members = True


# create the client with logs enabled
client = discord.Client(intents=intents)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')
token = os.getenv("DISCORD_TOKEN")

# run the bot
bot = commands.Bot(command_prefix='!', intents=intents)
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')
    






bot.run(token)

