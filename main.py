import discord
from discord.ext import commands
import logging
from dotenv import load_dotenv
import os
import yt_dlp

#load the dotenv file and get the token
load_dotenv(verbose=True)
token = os.getenv('discord_token')

intents = discord.Intents.default()
intents.message_content = True
intents.typing = True
intents.members = True
intents.guild_messages = True
intents.voice_states = True

Secret_Roles = "Friends"

# create the client with logs enabled
client = discord.Client(intents=intents)
handler = logging.FileHandler(filename='logs.log', encoding='utf-8', mode='w')


# run the bot
bot = commands.Bot(command_prefix='!', intents=intents)


# make bot ready
@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

 
# it will trigger when a message is inapropriate sent in the server
@bot.event
async def on_message(message):
    if message.author == bot.user:
        return  

    if "madarchod" in message.content.lower():
        await message.channel.send(f'{message.author.mention}, Do not use the inapropriate word, Nigga.')

    await bot.process_commands(message)

# it will assign the role and remove

@bot.command()
@commands.has_permissions(manage_roles=True)
async def assign(ctx, member: discord.Member, role: discord.Role):
    role = discord.utils.get(ctx.guild.roles, name=role.name)

    if role is None:
        await ctx.send(f"Role '{role.name}' not found.")
        return

    await member.add_roles(role)
    await ctx.send(f"Role '{role.name}' assigned to {member.mention}.")

@bot.command()
@commands.has_permissions(manage_roles=True)
async def rmv(ctx, member: discord.Member, role: discord.Role):
    role = discord.utils.get(ctx.guild.roles, name=role.name)

    if role is None:
        await ctx.send(f"Role '{role.name}' not found.")
        return

    await member.remove_roles(role)
    await ctx.send(f"Role '{role.name}' removed from {member.mention}.")

# run the bot




# Music setup

@bot.command()
async def join(ctx):
    if ctx.author.voice is None:
        await ctx.send("You are not in a voice channel.")
        return

    channel = ctx.author.voice.channel

    if ctx.voice_client:
        await ctx.voice_client.move_to(channel)
    else:
        await channel.connect()


@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.voice_client.disconnect() # this allows to join and leave the bot in voice channel

@bot.command()
async def play(ctx, *, search):
    if ctx.author.voice is None:
        return await ctx.send("You are not in a voice channel.")
    
    if not ctx.voice_client:
        await ctx.author.voice.channel.connect()
    
    if ctx.voice_client.is_playing():
        ctx.voice_client.stop()

    await ctx.send(f"Searching for: {search}...")

    ydl_opts = {'format': 'bestaudio', 'noplaylist': 'True', 'default_search': 'ytsearch'}
    ffmpeg_opts = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(search, download=False)
        if 'entries' in info:
            info = info['entries'][0]
        
        url = info['url']
        title = info['title']
        
        source = discord.FFmpegPCMAudio(url, **ffmpeg_opts)
        ctx.voice_client.play(source)
        await ctx.send(f"Now playing: **{title}**")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Stopped music.")





bot.run(token, log_handler=handler, log_level=logging.DEBUG)
