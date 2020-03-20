import os
import discord
from discord.ext.commands import Bot
from classes.User import User


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
async def my_research(ctx, param):
    u = User(ctx.author)
    for index,x in enumerate(param.split(',')):
        try:
            if isinstance(int(x), int):
                u.updateResearch(index, x)
        except ValueError:
            errorMessage = 'Tu ne m\'as pas donnée de niveau pour les {0}'
            switcher={
                0: 'RS',
                1: 'BS',
                2: 'WS',
            }
            errorVal = switcher.get(index, 'what?')
            await ctx.author.send(content=errorMessage.format(errorVal))
            return

    await ctx.author.send(content='Merci, j\'ai mis a jour tes données sur les recherches !') 

@bot.command()
async def helpBot(ctx):
    helpcommand = discord.Embed(
        title = 'Voici les commandes pour le bot {0}'.format(ctx.author.name),
        color = discord.Color.orange(),
    )
    helpcommand.add_field(name='!create_RS Niveau', value='Lance une invite pour les joueurs ayant le niveau requis', inline=False)
    helpcommand.add_field(name='!my_research RS,BS,WS', value='Met a jours toutes tes recherches', inline=False)
    helpcommand.set_author(name='Ton ami le bot !')
    helpcommand.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=helpcommand)

@bot.event
async def on_command_error(ctx, error):
    await ctx.send(content='Hey {0}, désolé je n\'ai pas compris ta demande. Essaye avec la commande !helpBot pour plus d\'information'.format(ctx.message.author.name))

@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title = 'Bienvenue chez BattleSquaddron {0}'.format(member.display_name)
    )
    embed.set_thumbnail(url=member.avatar_url)
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
