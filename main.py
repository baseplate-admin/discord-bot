import discord
from discord.ext import commands
import random
import asyncio
from discord.ext import tasks
from itertools import cycle
import json
import urllib.parse
import urllib.request
import re
import youtube_dl
import glob
import os
import time
import sched
# Youtube Play Music Important stuffs which i dont know

youtube_dl.utils.bug_reports_message = lambda: ''

ytdl_format_options = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}

ffmpeg_options = {
    'options': '-vn'
}

ytdl = youtube_dl.YoutubeDL(ytdl_format_options)


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data

        self.title = data.get('title')
        self.url = data.get('url')

    @classmethod
    async def from_url(cls, url, *, loop=None, stream=False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(None, lambda: ytdl.extract_info(url, download=not stream))

        if 'entries' in data:
            # take first item from a playlist
            data = data['entries'][0]

        filename = data['url'] if stream else ytdl.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data=data)

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
    query_string = urllib.parse.urlencode({
        'search_query': search
    })
    htm_content = urllib.request.urlopen(
        'https://www.youtube.com/results?' + query_string
    )
    search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
    search_result=('https://www.youtube.com/watch?v=' + search_results[0])
    if 
    if not ctx.message.author.voice:
        await ctx.send("You are not connected to a voice channel")
        return

    else:
        channel = ctx.message.author.voice.channel

    await channel.connect()

    server = ctx.message.guild
    voice_channel = server.voice_client

    async with ctx.typing():
        player = await YTDLSource.from_url(search_result, loop=client.loop)
        voice_channel.play(player, after=lambda e: print('Player error: %s' %e) if e else None)
    await ctx.send(f'Now Playing:{player.title}')

#Leave

@client.command(name='leave', help='This command stops makes the bot leave the voice channel')
async def leave(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()

# Python to destroy webp after every 5 min
@client.command()
async def clear_temp(ctx):
    z = 0
    x = []
    for file in os.listdir():
        if file.endswith('.webm'):
            x.append(file)
            z += 1
    await ctx.send("the total number of files: " + str(z))
    await ctx.send("Deleting these files.")
    await ctx.send(x)
    for i in glob.glob("*.webm"):
        os.remove(i)

# Count WebM Files
@client.command()
async def count(ctx):
    i = 0
    x = []
    for file in os.listdir():
        if file.endswith('.webm'):
            i += 1
    await ctx.send('the total number of files: ' + str(i))
client.run("NzUwMzY4OTAxNDYzODAxOTg3.X05hfw.u3i5EeUFfpuwof7tJiUXPvs_vWQ")
