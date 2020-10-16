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

@client.command()
async def loopqueue(ctx, *, search):
    def youtube_search(search):
        query_string