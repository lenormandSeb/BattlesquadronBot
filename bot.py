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

@bot.command()
async def helpBot(ctx):
    helpcommand = discord.Embed(
        title = 'Voici les commandes pour le bot',
        color = discord.Color.orange(),
    )
    helpcommand.add_field(name='!create_RS Niveau', value='Lance une invite pour les joueurs ayant le niveau requis', inline=True)
    helpcommand.set_author(name='Help')
    await ctx.send(content='{0}'.format(ctx.author.name), embed=helpcommand)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(content='Hey {0}, désolé je n\'ai pas compris ta demande. Essaye avec la commande !helpBot pour plus d\'information'.format(ctx.message.author.name))

@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title = 'Bienvenue chez BattleSquaddron {0}'.format(member.display_name)
    )
    embed.add_field(name='Qui suis-je ?', value='Je suis le bot de Battle Squadron', inline=False)
    embed.add_field(name='Qui sais-je faire ?', value='Tape !helpBot !', inline=False)
    await member.send(embed=embed)

    newEmbed = discord.Embed(
        title = 'J\'ai encore besoin de quelque info {0}'.format(member.display_name)
    )
    newEmbed.add_field(name='Quel info j\'ai besoin ?', value='Juste de ton niveau de recherche des étoiles Rouge, Bleu et Blanche', inline=False)
    newEmbed.add_field(name='Comment me les dire ?', value='Entre la commande !my_research x,x,x, (les trois x correspondent a tes niveaux dans l\'ordre precedement sité', inline=False)
    await member.send(embed=newEmbed)

bot.run(Token)
