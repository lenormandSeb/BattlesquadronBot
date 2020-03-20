import os
import discord
from discord.ext.commands import Bot

f = open('env', 'r')

Token = f.readline()

bot = Bot(command_prefix="!")

@bot.command()
async def testBotMoi(ctx):
    if ctx.message.content.find('coucou'):
        message = "serieux, encore un coucou ?"
    else :
        message = ctx.message
    await ctx.send(content='coucou {0}, ton message est : {1}'.format(ctx.author.name, message))

bot.run(Token)
