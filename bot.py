import os
import discord
from tinydb import TinyDB, Query
from discord.ext.commands import Bot
from classes.User import User


f = open('env', 'r')
db = TinyDB('user_database.json')
QueryDB = Query()
Token = f.readline()
bot = Bot(command_prefix="!")
bot.remove_command('help')


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
    table = db.table('user')
    table.upsert(u.jsonify(), QueryDB.id_user == ctx.author.id)
    await ctx.author.send(content='Merci, j\'ai mis a jour tes données sur les recherches !') 

@bot.command()
async def update_research(ctx, params):
    parameter = params.split(',')
    u = User(ctx.author)
    if parameter[0] == 'RS':
        research = 'Red Star'
        u.updateRedStar(parameter[1])
    elif parameter[0] == 'BS':
        research = 'Blue Star'
        u.updateBlueStar(parameter[1])
    elif parameter[0] == 'WS':
        research = 'White Star'
        u.updateWhiteStar(parameter[1])
    else:
        await ctx.channel.send(content='Désolé {0}, mais je ne connais pas la recherche {1}'.format(ctx.author.name, parameter[0]))
        return
    
    await ctx.channel.send(content='Ok {0}, j\'ai mis a jour ta recherche pour les {1}'.format(ctx.author.name, research))



@bot.command(pass_context=True)
async def help(ctx):
    helpcommand = discord.Embed(
        title = 'Voici les commandes pour le bot {0}'.format(ctx.author.name),
        color = discord.Color.orange(),
    )
    helpcommand.add_field(name='!create_RS Niveau', value='Lance une invite pour les joueurs ayant le niveau requis', inline=False)
    helpcommand.add_field(name='!my_research RS,BS,WS', value='Met a jours toutes tes recherches', inline=False)
    helpcommand.add_field(name='!update_research (RS ou BS ou WS),niveau', value='Met a jours la recherche défini', inline=False)
    helpcommand.set_author(name='Ton ami le bot !')
    helpcommand.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=helpcommand)

@bot.event
async def on_command_error(ctx, error):
    print(error)
    await ctx.send(content='Hey {0}, désolé je n\'ai pas compris ta demande. Essaye avec la commande !help pour plus d\'information'.format(ctx.message.author.name))

@bot.event
async def on_member_join(member):
    embed = discord.Embed(
        title = 'Bienvenue chez BattleSquaddron {0}'.format(member.display_name)
    )
    embed.set_thumbnail(url=member.avatar_url)
    embed.add_field(name='Qui suis-je ?', value='Je suis le bot de Battle Squadron', inline=False)
    embed.add_field(name='Qui sais-je faire ?', value='Tape !help !', inline=False)
    await member.send(embed=embed)

    newEmbed = discord.Embed(
        title = 'J\'ai encore besoin de quelque info {0}'.format(member.display_name)
    )
    newEmbed.add_field(name='Quel info j\'ai besoin ?', value='Juste de ton niveau de recherche des étoiles Rouge, Bleu et Blanche', inline=False)
    newEmbed.add_field(name='Comment me les dire ?', value='Entre la commande !my_research x,x,x, (les trois x correspondent a tes niveaux dans l\'ordre precedement sité', inline=False)
    await member.send(embed=newEmbed)

bot.run(Token)
