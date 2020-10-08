import discord
from discord.ext import commands
import random
from discord.ext import tasks
from itertools import cycle
import urllib.parse
import urllib.request
import re
import youtube_dl
import os
from discord.utils import get
import json
import shutil
from datetime import datetime
queues = {}
# Get prefix

volume = 100
volume_int = int(volume)
VOLUME_CONTROL = float(volume_int/100)

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
async def on_member_remove(member):
    print(f'{member} has been kicked from the server!! We will not miss him')


#   On member Add
@client.event
async def on_member_join(member):
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

    # TIME AND DATE
    obj_now = datetime.now()

    hour = obj_now.hour
    minute = obj_now.minute
    second = obj_now.second
    microsecond = obj_now.microsecond

    time = (f"{hour}:{minute}:{second}.{microsecond}")

    from datetime import date
    import calendar
    my_date = date.today()
    x = calendar.day_name[my_date.weekday()]

    from datetime import date

    today = date.today()
    d2 = today.strftime("%B %d, %Y")

    string = x + " " + d2

    dict = {
        "url" : search_result,
        "query": search,
        "time": time,
        "day": string,
    }
    with open('result.json', 'a') as fp:
        json.dump(dict, fp, indent=2)

    # Checks and connects to user voice channel
    global voice_check
    channel_check = ctx.message.author.voice.channel
    voice_check = get(client.voice_clients, guild=ctx.guild)
    if voice_check and voice_check.is_connected():
        await voice_check.move_to(channel_check)
    else:
        voice_check = await channel_check.connect()


    if voice_check and voice_check.is_playing():
        Queue_infile = os.path.isdir("./Queue")
        if Queue_infile is False:
            os.mkdir("Queue")
        DIR = os.path.abspath(os.path.realpath("Queue"))
        q_num = len(os.listdir(DIR))
        q_num += 1
        add_queue = True
        while add_queue:
            if q_num in queues:
                q_num += 1
            else:
                add_queue = False
                queues[q_num] = q_num
        queue_path = os.path.abspath(os.path.realpath("Queue") + f"\song{q_num}.%(ext)s")
        ydl_options = {
            "format": "bestaudio/best",
            "outtmpl": queue_path,
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "320",
            }],
        }
        with youtube_dl.YoutubeDL(ydl_options) as ydl:
            print("Downloading audio now!\n")
            ydl.download([search_result])
        await ctx.send("Adding " + search + " to the queue")
        print("Song Added to queue\n")

    else:
        def check_queue():
            Queue_infile = os.path.isdir("./Queue")
            if Queue_infile is True:
                DIR = os.path.abspath(os.path.realpath("Queue"))
                length = len(os.listdir(DIR))
                still_q = length - 1
                try:
                    first_file = os.listdir(DIR)[0]
                except:
                    print("No queued song(s)\n")
                    queues.clear()
                    return
                main_location = os.path.dirname(os.path.realpath(__file__))
                song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                if length != 0:
                    print("Song done, playing next queued\n")
                    print(f"Songs still in queue: {still_q}")
                    song_there = os.path.isfile("song.mp3")
                    if song_there:
                        os.remove("song.mp3")

                    shutil.move(song_path, main_location)
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            os.rename(file, "song.mp3")
                    voice.play(discord.FFmpegPCMAudio('song.mp3'), after=lambda e: check_queue())
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = VOLUME_CONTROL
                else:
                    queues.clear()
                    return
            else:
                queues.clear()
                print("No songs were queued before")
        song_there = os.path.isfile("song.mp3")
        try:
            if song_there:
                os.remove("song.mp3")
                queues.clear()
                print("Removing old song file")
        except PermissionError:
            print("Trying to delete songs, but its being played")
            await ctx.send("ERROR:MUSIC PLAYING.")
            return
        Queue_infile = os.path.isdir("./Queue")
        try:
            Queue_folder = "./Queue"
            if Queue_infile is True:
                print("Removed old Queue Folder")
                shutil.rmtree(Queue_folder)
        except:
            print("No old Queue folder.")

        #Downloading
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
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
        newname = name.rsplit("-", 2)
        await ctx.send(f"Playing, {newname[1]}")
        print("Playing song\n")
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: check_queue())
        voice.source = discord.PCMVolumeTransformer(voice.sources)
        voice.sources.volume = VOLUME_CONTROL



# Queue Function

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

#Skip Function
@client.command()
async def skip(ctx):
    voices = get(client.voice_clients, guild=ctx.guild)
    queues.clear()
    if voices and voices.is_playing():
        print("Music Skipped")
        voices.stop()
        await ctx.send("Music Skipped")
    else:
        print("No music to skip")
        await ctx.send("No music")


client.run("NzUwMzY4OTAxNDYzODAxOTg3.X05hfw.EjbHhDGwxEJIzVdrBFgeGPM88TE")


## TODO ?
# 1. Add COGS
# 2. Add Loop Function
# 3. Profit?
# add reactions