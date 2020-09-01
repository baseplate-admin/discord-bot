import discord
from discord.ext import commands

client = commands.Bot(command_prefix="`")

@client.event
async def on_ready():
    print("I am created by Baseplate-Admin. Woo Hoo!!!")

@client.event
async def on_member_join(member):
    print(f'{member} joined the server.')

@client.event
async def on_member_leave(member):
    print(f'{member} left the server')

@client.command(aliases=["PING","ping"])
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency * 1000)}ms')


@client.command(aliases=['8ball'])
async def _8ball():

client.run("NzUwMzY4OTAxNDYzODAxOTg3.X05hfw._68r_8F-382WVogaW4kV2N96uHc")