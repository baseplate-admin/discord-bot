import discord
from discord.ext import commands
import random
client = commands.Bot(command_prefix=".")

#   Discord Events!!
#   Event Loop
@client.event
async def on_ready():
    print("I am a bot and created by BasePlate-Admin!! Woo Hoo!!")

#   On member kick
@client.event
async def on_member_remove():
    print(f'{member} has been kicked from the server!! We will not miss him')
#   On member Add
@client.event
async def on_member_join():
    print(f"{member} has joined TFB!! Lets Welcome him.")
#   Client Commands!!!
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
async def clear(ctx, amount=0):
    await ctx.channel.purge(limit=amount)
# Clear All Chat
@client.command(aliases=['clearchatall'])
async def chatclearall(ctx,
                       amount=9999999999999):
    await ctx.channel.purge(limit=amount)

# Kicking
@client.command(aliases=["sayonara"])
async def byebye(ctx, member : discord.Member, * ,reason=None):
    await member.kick(reason=reason)
# Ban
@client.command(aliases=["fuck_you","jail"])
async def gotojail(ctx, member : discord.Member, * , reason=None):
    await member.ban(reason=reason)

client.run("")