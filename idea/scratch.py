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























    client.run(TOKEN)