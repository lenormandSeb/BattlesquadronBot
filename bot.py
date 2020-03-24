import os
import discord
from tinydb import TinyDB, Query
from discord.ext.commands import Bot
from classes.User import User
from dotenv import load_dotenv

load_dotenv()
db = TinyDB('user_database.json')
QueryDB = Query()
Token = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix="!")
bot.remove_command('help')

@bot.event
async def on_ready():
    game = discord.Game("avec des Humains !")
    await bot.change_presence(status=discord.Status.idle, activity=game)

@bot.command()
async def create_RS(ctx, lvl, hour = None):
    author = ctx.author.name
    if lvl != '0':
        table = db.table('user')
        search = table.search(QueryDB.RS >= lvl)

        if hour:
            message = ' pour {0}'.format(hour)
        else:
            message = ''

        if len(search) > 0:
            for result in search:
                forsend = bot.get_user(result.get('id_user'))
                name = result.get('name')
                await forsend.send(content='Hey {0}, {1} lance une RS {2}{3}, seras-tu présent(e) ? '.format(name, author, lvl, message))
        else:
            await ctx.send(content='Désoler {0}, mais personne n\'as débloquer ce niveau de recherche'.format(author))
        message = await ctx.send(content='{0}, tu veux creer une RS de niveau {1}? J\'envoie une invite a ceux qui le peuvent'.format(author, lvl))
        await ctx.message.add_reaction('👍')
    else:
        await ctx.send(content='{0}, cela n\'existe pas une RS 0'.format(author))


@bot.command()
async def my_research(ctx, param):
    u = User(ctx.author)
    try:
        if isinstance(int(param), int):
            u.updateRedStar(param)
    except ValueError:
        errorMessage = 'Tu ne m\'as pas donnée de niveau pour la recherche'
        await ctx.author.send(content=errorMessage)
        return
    table = db.table('user')
    table.upsert(u.jsonify(), QueryDB.id_user == ctx.author.id)
    await ctx.author.send(content='Merci, j\'ai mis a jour tes données sur les recherches !') 

@bot.command(pass_context=True)
async def help(ctx):
    helpcommand = discord.Embed(
        title = 'Voici les commandes pour le bot {0}'.format(ctx.author.name),
        color = discord.Color.orange(),
    )
    helpcommand.add_field(name='!create_RS Niveau Heure(optionel)', value='Lance une invite pour les joueurs ayant le niveau requis avec l\'heure ou sans. \n Exemple: `!create_RS 2`, `!create_RS 2 20h`', inline=False)
    helpcommand.add_field(name='!my_research niveau_recherche_RS', value='Met a jours ton niveau de recherche étoile rouge.\n Exemple: `!my_research 1`', inline=False)
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
    newEmbed.add_field(name='Quel info j\'ai besoin ?', value='Juste de ton niveau de recherche des étoiles Rouge', inline=False)
    newEmbed.add_field(name='Comment me les dire ?', value='Entre la commande !my_research x (le x correspond a ton niveaux de recherche du scanneur étoile rouge', inline=False)
    await member.send(embed=newEmbed)

bot.run(Token)
