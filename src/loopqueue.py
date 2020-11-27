def main_function_discord(TOKEN):
    import discord
    from discord.ext import commands
    import random
    import asyncio
    import urllib.parse
    import urllib.request
    import re
    import youtube_dl
    import os
    from discord.utils import get
    import json
    import shutil
    from datetime import datetime
    import glob
    from bs4 import BeautifulSoup
    import calendar
    from .crypto import encrypt, decrypt

    # QUEUE DICTIONARY
    queues = {}

    # Song Number

    global songNumber
    songNumber = 0

    # Volume Control

    volume = 100
    volume_int = int(volume)
    VOLUME_CONTROL = float(volume_int / 100)


    # Get prefix

    def get_prefix(client, message):
        if os.path.isfile("result.ejson") or os.path.isfile("prefixes.ejson"):
            decrypt("result.ejson")
            decrypt("prefixes.ejson")
        jsons = open("prefixes.json", "r")
        prefixes = json.load(jsons)
        return prefixes[str(message.guild.id)]


    client = commands.Bot(command_prefix=get_prefix)

    @client.event
    async def on_ready():
        if os.path.isfile("result.ejson") or os.path.isfile("prefixes.ejson"):
            decrypt("result.ejson")
            decrypt("prefixes.ejson")
        else:
            pass
        print("I am a bot and created by BasePlate-Admin!! Woo Hoo!!")


    async def game_presence():
        await client.wait_until_ready()

        game = ["I am a bot!", "Life in python,Its fantastic", "Fun!!"]
        while not client.is_closed():
            status = random.choice(game)
            await client.change_presence(activity=discord.Game(status))
            await asyncio.sleep(10)
    client.loop.create_task(game_presence())

    @client.command()
    async def play(ctx, *, search):
        if os.path.isfile("result.ejson") or os.path.isfile('prefixes.ejson'):
            decrypt("result.ejson")
            decrypt("prefixes.ejson")
        if not ctx.message.author.voice:
            await ctx.send("You are not connected to a voice channel")
            return
        else:
            def search_youtube(query):
                query_string = urllib.parse.urlencode({
                    'search_query': query,
                })
                htm_content = urllib.request.urlopen(
                    'https://www.youtube.com/results?' + query_string
                )
                search_results = re.findall(r'/watch\?v=(.{11})', htm_content.read().decode())
                search_result_1 = ('https://www.youtube.com/watch?v=' + search_results[0])
                return search_result_1

            # TIME AND DATE
            def telementry(link):
                obj_now = datetime.now()

                hour = obj_now.hour
                minute = obj_now.minute
                second = obj_now.second
                microsecond = obj_now.microsecond

                time = (f"{hour}:{minute}:{second}.{microsecond}")

                from datetime import date

                my_date = date.today()
                x = calendar.day_name[my_date.weekday()]

                from datetime import date

                today = date.today()
                d2 = today.strftime("%B %d, %Y")

                string = x + " " + d2

                dict = {
                    "url": link,
                    "query": search,
                    "time": time,
                    "day": string,
                    "type": "play",
                }
                with open('result.json', 'a') as fp:
                    json.dump(dict, fp, indent=2)

            ## TIME KILL FUNTION
            def time_wait(seconds):
                import time
                time.sleep(seconds)

            # Checks and connects to user voice channel
            ## CANNOT BE PARALLELIZED
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
                    ydl.download([search_youtube(search)])
                await ctx.send("Adding " + search + " to the queue")
                print("Song Added to queue\n")

            else:
                def check_queue():
                    voice = get(client.voice_clients, guild=ctx.guild)
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
                        main_location = os.getcwd()
                        song_path = os.path.abspath(os.path.realpath("Queue") + "\\" + first_file)
                        if length != 0:
                            print("Song done, playing next queued\n")
                            print(f"Songs still in queue: {still_q}")
                            for files in os.listdir(os.getcwd()):
                                song_there = os.path.isfile("zad.mp3")
                                if song_there:
                                    os.remove("zad.mp3")

                            shutil.move(song_path, main_location)
                            for file in os.listdir("./"):
                                if file.endswith(".mp3"):
                                    os.rename(file, "zad.mp3")
                            voice.play(discord.FFmpegPCMAudio('zad.mp3'), after=lambda e: check_queue())
                            voice.source = discord.PCMVolumeTransformer(voice.source)
                            voice.source.volume = VOLUME_CONTROL
                        else:
                            queues.clear()
                            return
                    else:
                        queues.clear()
                        print("No songs were queued before")

                def song_and_queue_check():
                    song_there = os.path.isfile("zad.mp3")
                    try:
                        if song_there:
                            os.remove("zad.mp3")
                            queues.clear()
                            print("Removing old song file")
                    except PermissionError:
                        print("Trying to delete songs, but its being played")
                        # await ctx.send("ERROR:MUSIC PLAYING.")
                        return
                    Queue_infile = os.path.isdir("./Queue")
                    try:
                        Queue_folder = "./Queue"
                        if Queue_infile is True:
                            print("Removed old Queue Folder")
                            shutil.rmtree(Queue_folder)
                    except:
                        print("No old Queue folder.")

                # Downloading

                def play_song(link):
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
                        ydl.download([link])
                    for file in os.listdir("./"):
                        if file.endswith(".mp3"):
                            print(f"Renamed File: {file}\n")
                            os.rename(file, "zad.mp3")
                    # Play SONG LOGIC
                    voice = get(client.voice_clients, guild=ctx.guild)

                    print("Playing song\n")
                    voice.play(discord.FFmpegPCMAudio("zad.mp3"), after=lambda e: check_queue())
                    # END LOGIC
                    # Reaction LOGIC

                    voice.source = discord.PCMVolumeTransformer(voice.sources)
                    voice.sources.volume = VOLUME_CONTROL
                    # END LOGIC

                ## CALLS ALL THE FUNCTION
                # BS4 Search LOGIC
                link = search_youtube(search)

                def bs4_GET_TITLE(link):
                    page = urllib.request.urlopen(link)
                    html = BeautifulSoup(page.read(), "html.parser")
                    bs4_title_1 = html.title.string
                    return bs4_title_1

                # Logic Ends Here

                ## SEND REACTION LOGIC
                bs4_title = bs4_GET_TITLE(link)
                await ctx.send(f"Playing, {bs4_title}")
                await ctx.message.add_reaction("▶️")

                ## LOGIC ENDS HERE

                ## MULTIPROCESS LOGIC

                def multiprocessing(link):
                    import time
                    from concurrent.futures import ThreadPoolExecutor
                    with ThreadPoolExecutor(max_workers=3) as executor:
                        to_do = [executor.submit(song_and_queue_check),
                                 executor.submit(play_song, link),
                                 executor.submit(telementry, link)]

                ## END FUNCTION CALL
                multiprocessing(link)
    client.run(TOKEN)