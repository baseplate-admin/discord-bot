import discord
from discord.ext import commands
import random
import os
from discord.ext import tasks
from itertools import cycle
import json

# Get prefix

def get_prefix(client, message):
    jsons = open("prefixes.json", "r")
    prefixes = json.load(jsons)
    return prefixes[str(message.guild.id)]

client = commands.Bot(command_prefix = get_prefix)
status = cycle(["I am a bot!", "Life in python,Its fantastic", "Fun!!"])
bot = commands.Bot(command_prefix = get_prefix)

#   Discord Events!!

@client.event
async def on_ready():
    change_status.start()
    print("I am a bot and created by BasePlate-Admin!! Woo Hoo!!")
    client.load_extension(f"cogs.music")

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


# Cog
@client.command()
async def load(ctx):
    client.load_extension(f"cogs.music")

# Unload
@client.command()
async def unload(ctx):
    client.unload_extension(f"cogs.music")

@client.command()
async def leavevoice(ctx):
    for x in client.voice_clients:
        if(x.server == ctx.message.server):
            return await x.disconnect()

    return await client.say("I am not connected to any voice channel on this server!")
# Error

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("How many message should I delete? I am a bot not a human")

# Task Loop

@tasks.loop(seconds=10)
async def change_status():
    await client.change_presence(activity=discord.Game(next(status)))

client.run("")