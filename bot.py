import os
import discord
from discord.ext.commands import Bot

f = open('env', 'r')

Token = f.readline()
bot = Bot(command_prefix="!")


@bot.command()
async def create_RS(ctx, lvl):
    author = ctx.author.name
    if lvl != '0':
        await ctx.send(content='{0}, tu veux creer une RS de niveau {1}? J\'envoie une invite a ceux qui le peuvent'.format(author, lvl))
    else:
        await ctx.send(content='{0}, cela n\'existe pas une RS 0'.format(author))


@bot.command()
async def testBotMoi(ctx):
    if ctx.message.content.find('coucou'):
        message = "serieux, encore un coucou ?"
    else :
        message = ctx.message
    await ctx.send(content='coucou {0}, ton message est : {1}'.format(ctx.author.name, message))

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(content='Hey {0}, désolé je n\'ai pas compris ta demande. Essaye avec la commande !help pour plus d\'information'.format(ctx.message.author.name))

bot.run(Token)
