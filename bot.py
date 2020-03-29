import os
import discord
import re
from tinydb import TinyDB, Query
from discord.ext.commands import Bot
from classes.User import User
from classes.Cruiser import Cruiser
from dotenv import load_dotenv

load_dotenv()
db = TinyDB(os.getenv('PATH_BDD') + 'bdd/user_database.json')
QueryDB = Query()
Token = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix="!")
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)

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
                try:
                    await forsend.send(content='Hey {0}, {1} lance une RS {2}{3}, seras-tu présent(e) ? '.format(name, author, lvl, message))
                except discord.HTTPException:
                    await ctx.channel.send(content='Hey @{0}, {1} lance une RS {2}{3}, seras-tu présent(e) ? '.format(name, author, lvl, message))
        else:
            await ctx.send(content='Désoler {0}, mais personne n\'as débloquer ce niveau de recherche'.format(author))
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
        try:
            await ctx.author.send(content=errorMessage)
        except discord.HTTPException:
            await ctx.channel.send(content='Tu ne m\'as pas donnée de niveau pour la recherche {0}'.format(ctx.author.name))
        return
    table = db.table('user')
    table.upsert(u.jsonify(), QueryDB.id_user == ctx.author.id)
    try:
        await ctx.author.send(content='Merci, j\'ai mis a jour tes données sur les recherches !')
    except discord.HTTPException:
        await ctx.channel.send(content='Merci {0}, j\'ai mis a jour tes données sur les recherches !'.format(ctx.author.name))

@bot.command()
async def infrs(ctx, param):
    try:
        table = db.table('user')
        search = table.search(QueryDB.name.matches(param, flags=re.IGNORECASE))
        if len(search) > 0:
            message = 'Le niveau de RS de {0} est : {1}'.format(param, search[0]['RS'])
            await ctx.channel.send(content=message)
        else:
            await ctx.channel.send(content='Désoler mais je n\'ai trouvé personne')
    except:
        await ctx.channel.send(content='Désoler mais tu ne m\'as donné aucun nom')

@bot.command()
async def my_ship(ctx):
    table = db.table('spaceShip')
    search = table.search(QueryDB.id_user == ctx.author.id)
    if (len(search)):
        ship = discord.Embed(
            title = 'Tes Cuirasiers {}'.format(ctx.author.name)
        )
        for s in search:
            ship.add_field(name='Nom :', value=s.get('ship_name'), inline=True)
            ship.add_field(name='Module : ', value=s.get('module'), inline=False)
            ship.add_field(name='-----', value='-----', inline=False)
        await ctx.channel.send(embed=ship)
    else:
        await ctx.channel.send(content='Tu n\'as pas de vaisseaux enregistré')

@bot.command()
async def add_cruiser(ctx, name=None):
    if name == None:
        errorMessage = 'Ton cuirassé n\'as pas de nom'
        try:
            await ctx.author.send(content=errorMessage)
        except discord.HTTPException:
            await ctx.channel.send(content='Ton cuirassé n\'as pas de nom {0}'.format(ctx.author.name))
        return
    else:
        cruiser = Cruiser(ctx.author, name)
        table = db.table('spaceShip')
        table.upsert(cruiser.jsonify(), (QueryDB.id_user == ctx.author.id) & (QueryDB.ship_name == name))
        embed_ship = discord.Embed(
            title = 'Ajout de {0}'.format(name),
            color = discord.Color.red(),
        )
        await ctx.channel.send(embed=embed_ship)

@bot.command()
async def destroy_cruiser(ctx, name=None):
    if name == None:
        errorMessage = 'Ton cuirassé n\'as pas de nom'
        try:
            await ctx.author.send(content=errorMessage)
        except discord.HTTPException:
            await ctx.channel.send(content='Ton cuirassé n\'as pas de nom {0}'.format(ctx.author.name))
        return
    else:
        table = db.table('spaceShip')
        search = table.search((QueryDB.id_user == ctx.author.id) & (QueryDB.ship_name.matches(name, flags=re.IGNORECASE)))
        if (len(search)):
            table.remove(doc_ids=[search[0].doc_id])
            await ctx.channel.send(content="Au revoir p'tit vaisseaux")
        else:
            await ctx.channel.send(content='Pas de vaisseau trouvé pour {}'.format(name))

@bot.command(pass_context=True)
async def help(ctx):
    helpcommand = discord.Embed(
        title = 'Voici les commandes pour le bot {0}'.format(ctx.author.name),
        color = discord.Color.orange(),
    )
    helpcommand.add_field(name='!create_RS Niveau Heure(optionel)', value='Lance une invite pour les joueurs ayant le niveau requis avec l\'heure ou sans. \n Exemple: `!create_RS 2`, `!create_RS 2 20h`', inline=False)
    helpcommand.add_field(name='!my_research niveau_recherche_RS', value='Met a jours ton niveau de recherche étoile rouge.\n Exemple: `!my_research 1`', inline=False)
    helpcommand.add_field(name='!infrs nom_du_joueur', value='Recherche le niveau de RS d\'un joueur.\n Exemple: `!infrs kirino`', inline=False)
    helpcommand.add_field(name='!my_ship', value='Retrouve tous tes vaisseaux.\n', inline=False)
    helpcommand.add_field(name='!add_cruiser Nom_du_vaisseau', value='Ajout un nouveau vaisseau.\n Exemple `!add_cruiser NCC-1701`', inline=False)
    helpcommand.add_field(name='!destroy_cruiser Nom_du_vaisseau', value='Supprime un vaisseau.\n Exemple `!destroy_cruiser NCC-1701`', inline=False)
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

    try:
        await member.send(embed=embed)
    except discord.HTTPException:
        return

    newEmbed = discord.Embed(
        title = 'J\'ai encore besoin de quelque info {0}'.format(member.display_name)
    )
    newEmbed.add_field(name='Quel info j\'ai besoin ?', value='Juste de ton niveau de recherche des étoiles Rouge', inline=False)
    newEmbed.add_field(name='Comment me les dire ?', value='Entre la commande !my_research x (le x correspond a ton niveaux de recherche du scanneur étoile rouge', inline=False)

    try:
        await member.send(embed=newEmbed)
    except discord.HTTPException:
        return


bot.run(Token)
