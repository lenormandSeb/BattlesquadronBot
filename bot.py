import os
import discord
from discord.ext.commands import Bot

bot = Bot(command_prefix="!")

@bot.command()
async def testBotMoi(ctx):
    if ctx.message.content.find('coucou'):
        message = "serieux, encore un coucou ?"
    else :
        message = ctx.message
    await ctx.send(content='coucou {0}, ton message est : {1}'.format(ctx.author.name, message))

bot.run("NjkwNTg5MTg3Mjk2MTk4NzY2.XnT27Q.Q637X9tRc0gG_I8QIQf2-8k_oOQ")
