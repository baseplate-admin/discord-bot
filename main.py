import discord
from discord.ext import commands
import random
import asyncio
from discord.ext import tasks
from itertools import cycle
import urllib.parse
import urllib.request
import re
import youtube_dl
import glob
import os
from discord.utils import get
import json
# Get prefix

def get_prefix(client, message):
    jsons = open("prefixes.json", "r")
    prefixes = json.load(jsons)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
bot = commands.Bot(command_prefix = get_prefix)
status = cycle(["I am a bot!", "Life in python,Its fantastic", "Fun!!"])

#   Discord Events!!

@client.event
async def on_ready():
    change_status.start()
    print("I am a bot and created by BasePlate-Admin!! Woo Hoo!!")


# Error
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
      await ctx.send("Whatcha doin mate? I dont know this command.")

#   On member kick
@client.event
async def on_member_remove():
    print(f'{member} has been kicked from the server!! We will not miss him')


#   On member Add
@client.event
async def on_member_join():
    print(f"{member} has joined TFB!! Lets Welcome him.")

# Prefix events

#Guild Join
@client.event
async def on_guild_join(guild):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes[str(guild.id)] = "."

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

#Guild Leave
@client.event
async def on_guild_remove(guild):
    with open ("prefixes.json", "r") as f:
        prefixes = json.load(f)

    prefixes.pop(str(guild.id))

    with open("prefixes.json", "w") as f:
        json.dump(prefixes, f, indent=4)

#   Client Commands!!!
#   Change Prefix
@client.command()
async def changeprefix(ctx, prefix):
    with open('prefixes.json', 'r') as f:
        prefixes = json.load(f)

    prefixes[str(ctx.guild.id)] = prefix
    with open('prefixes.json', 'w') as f:
        json.dump(prefixes, f, indent=4)

    await ctx.send(f'Prefix changed to: {prefix}')

#   Ping Command
@client.command()
async def ping(ctx):
    await ctx.send(f"Pong! {round(client.latency * 1000)}ms")


#   Luck Generator
@client.command(aliases=['luckgen'])
async def _8ball(ctx, *, question):
    responses=[
        "It is certain.",
        "It is decidely so.",
        "Without a doubt.",
        "Yes - Definitely",
        "You may rely on it.",
        "As I see it,yes.",
        "Most Likely.",
        "Outlook good.",
        "Yes.",
        "Signs point to yes.",
        "Reply Hazy try agin mate.",
        "Ask again later.",
        "Better not tell you now.",
        "Cant predict now.",
        "Concentrate and try again.",
        "Dont count on it.",
        "My reply is no.",
        "Sources say no.",
        "Outlook not so good.",
        "Very Doubtful."
    ]
    await ctx.send(f'Questions: {question} \n Answer: {random.choice(responses)}')


# Clear Chat
@client.command()
@commands.has_role("Management")
async def clear(ctx, amount : int):
    await ctx.channel.purge(limit=amount)


# Clear All Chat

@client.command(aliases=['clearchatall'])
@commands.has_role("Management")
async def chatclearall(ctx,
                       amount=9999999999999):
    await ctx.channel.purge(limit=amount)


# Kicking
@client.command(aliases=["sayonara"])
@commands.has_role("Management")
async def byebye(ctx, member : discord.Member, * ,reason=None):
    await member.kick(reason=reason)
    await ctx.send(f'{member.mention} is naughty. We dont want him in our server!!')


# Ban
@client.command(aliases=["fuck_you","jail"])
@commands.has_role("Management")
async def gotojail(ctx, member : discord.Member, * , reason=None):
    await member.ban(reason=reason)
    await ctx.send(f'{member.mention}  has done a crime and admins sent him to jail.')

# Unban
@client.command()
async def unban(ctx, * ,member):
    find_ban = await ctx.guild.bans()
    mem_nem, mem_dis = member.split("#")
    for i in find_ban:
        user = i.user
        if (user.name, user.discriminator) == (mem_nem, mem_dis):
            await ctx.guild.unban(user)
            await ctx.send(f'Unbanned {user.mention} welcome back!!')
            return

# Error

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("How many message should I delete? I am a bot not a human")

# Task Loop

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

#Youtube Music

# Search Function
@client.command(aliases=[])
async def play(ctx, *, search):
    # Checks and connects to user voice channel
    global voice_check
    channel_check = ctx.message.author.voice.channel
    voice_check = get(client.voice_clients, guild=ctx.guild)
    if voice_check and voice_check.is_connected():
        await voice_check.move_to(channel_check)
    else:
        voice_check = await channel_check.connect()

    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    search_result=('https://www.youtube.com/watch?v=' + search_results[0])

    #Player Function

    # Remove Song MP3
    song_there = os.path.isfile("song.mp3")
    try:
        if song_there:
            os.remove("song.mp3")
    except PermissionError:
        print("Trying to delete song file but its being played.")
        await ctx.send("ERROR:Music Playing")
        return
    await ctx.send("Getting From Youtube.....")
    voice = get(client.voice_clients, guild=ctx.guild)
    ydl_options = {
        "format": "bestaudio/best",
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "320",
            }]
    }
    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        print("Downloading Audio Now\n")
        ydl.download([search_result])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            name = file
            print(f"Renamed file: {file}\n")
            os.rename(file, "song.mp3")
    voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print(f"{name} has finished playing"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.07

    newname = name.rsplit("-", 2)
    await ctx.send(f"Playing, {newname}")
    print("Playing song\n")
#Pause Function
@client.command()
async def pause(ctx):
    voice = get(client.voice_clients, guild=ctx.guild)
    if voice and voice.is_playing():
        await ctx.send("Music Paused")
        voice.pause()
    else:
        await ctx.send("Music not playing.")

# Resume Function
@client.command()
async def resume(ctx):
    voices = get(client.voice_clients, guild=ctx.guild)

    if voices and voices.is_paused():
        voices.resume()
        await ctx.send("Resuming player")
    else:
        await ctx.send("Music is not resumed")

# Stop Function
@client.command()
async def stop(ctx):
     voice_client = ctx.message.guild.voice_client
     await voice_client.disconnect()






client.run("")
