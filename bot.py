import os
import discord
import re
from tinydb import TinyDB, Query
from discord.ext.commands import Bot
import BotClass
from dotenv import load_dotenv

load_dotenv()
s = BotClass.Star()
db = TinyDB(os.getenv('PATH_BDD') + 'bdd/user_database.json')
QueryDB = Query()
Token = os.getenv('DISCORD_TOKEN')
bot = Bot(command_prefix="!")
bot.remove_command('help')

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.idle)

@bot.command()
async def rs(ctx, lvl, hour = None):
    author = ctx.author.name
    if lvl != '0':
        table = db.table('user')
        search = table.search(QueryDB.RS >= lvl)

        em = discord.Embed(
            title = 'Creation RS par {}'.format(author),
        )

        em.set_thumbnail(url='https://cdn.discordapp.com/attachments/691684927309348937/696077525562032188/redStar.png')
        em.add_field(name='Level Requis', value=lvl, inline=False)
        em.add_field(name='Créateur', value=author, inline=False)
        if hour:
            em.add_field(name='Heure de début', value=hour, inline=False)
        total = int(lvl) + 1
        em.add_field(name='Place disponible', value='{}/{}'.format(str(lvl), str(total)), inline=False)
        em.add_field(name='Participant', value=author, inline=False)

        if len(search) > 0:
            message = await ctx.channel.send(embed=em)
            # Insert into bdd
            table = db.table('eventRs')
            eventRs = {
                "id_event" : message.id,
                "author" : author,
                "author_id" : ctx.author.id,
                "hour" : hour if hour else None,
                "require_lvl": lvl,
                "place": str(total),
                "user" : [{
                    'name' : author
                }]
            }
            insert = table.upsert(eventRs, QueryDB.id_event == message.id)
        else:
            await ctx.send(content='Désoler {0}, mais personne n\'as débloquer ce niveau de recherche'.format(author))
    else:
        await ctx.send(content='{0}, cela n\'existe pas une RS 0'.format(author))

@bot.command()
async def my_research(ctx, param):
    u = BotClass.User(ctx.author)
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
    userToResearch = ctx.message.mentions[0].id
    try:
        table = db.table('user')
        search = table.search(QueryDB.id_user == userToResearch)
        if len(search) > 0:
            message = 'Le niveau de RS de {0} est : {1}'.format(ctx.message.mentions[0].name, search[0]['RS'])
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
        cruiser = BotClass.Cruiser(ctx.author, name)
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
    helpcommand.add_field(name='!rs Niveau Heure(optionel)', value='Lance une invite pour les joueurs ayant le niveau requis avec l\'heure ou sans. \n Exemple: `!rs 2`, `!rs 2 20h`', inline=False)
    helpcommand.add_field(name='!my_research niveau_recherche_RS', value='Met a jours ton niveau de recherche étoile rouge.\n Exemple: `!my_research 1`', inline=False)
    helpcommand.add_field(name='!infrs @nom_du_joueur', value='Recherche le niveau de RS d\'un joueur.\n Exemple: `!infrs @kirino`', inline=False)
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

@bot.event
async def on_raw_reaction_add(reaction):
    table = db.table('eventRs')
    search = table.search(QueryDB.id_event == reaction.message_id)
    channel = bot.get_channel(reaction.channel_id)
    message = await channel.fetch_message(reaction.message_id)
    if len(search) and reaction.emoji.name == '👍' :
        present = False
        for u in search[0].get('user'):
            if u['name'] == reaction.member.name:
                present = True
        if not present:
            user = bot.get_user(reaction.user_id)
            if not user.name in search[0].get('user') :
                total = int(search[0].get('require_lvl')) + 1
                dispo = (total - len(search[0].get('user')))
                if dispo > 0:
                    userToAdd = {
                        'name' : user.name
                    }
                    search[0].get('user').append(userToAdd)
                    update = {
                        'id_event':search[0].get('id_event'),
                        'user': search[0].get('user')
                    }
                    table.upsert(update, QueryDB.id_event == reaction.message_id)

                    lastEmbed = message.embeds[0]
                    newEmbed = discord.Embed(
                        title = lastEmbed.title
                    )

                    newEmbed.set_thumbnail(url=lastEmbed.thumbnail.url)
                    newEmbed.add_field(name='Level Requis', value=search[0].get('require_lvl'), inline=False)
                    newEmbed.add_field(name='Créateur', value=search[0].get('author'), inline=False)
                    if search[0].get('hour'):
                        newEmbed.add_field(name='Heure de début', value=search[0].get('hour'), inline=False)

                    participant = []
                    for u in search[0].get('user'):
                        participant.append(u['name'])
                    newEmbed.add_field(name='Place disponible', value='{}/{}'.format(str(dispo), str(total)), inline=False)
                    newEmbed.add_field(name='Participant', value=','.join(participant), inline=False)

                    await message.edit(embed=newEmbed)
        else:
            await message.remove_reaction(reaction.emoji, reaction.member)


@bot.event
async def on_raw_reaction_remove(reaction):
    table = db.table('eventRs')
    print(reaction)
    search = table.search(QueryDB.id_event == reaction.message_id)
    if reaction.member != None or reaction.user_id != search[0].get('author_id'):
        if len(search) and reaction.emoji.name == '👍' :
            user = bot.get_user(reaction.user_id)
            finduser = {'name' : user.name}
            if finduser in search[0].get('user') :
                toRemove = {
                    'name' : user.name
                }
                search[0].get('user').remove(toRemove)
                update = {
                    'id_event':search[0].get('id_event'),
                    'place':search[0].get('place'),
                    'user': search[0].get('user')
                }
                table.upsert(update, QueryDB.id_event == reaction.message_id)
                channel = bot.get_channel(reaction.channel_id)
                message = await channel.fetch_message(reaction.message_id)
                lastEmbed = message.embeds[0]
                newEmbed = discord.Embed(
                    title = lastEmbed.title
                )

                newEmbed.set_thumbnail(url=lastEmbed.thumbnail.url)
                newEmbed.add_field(name='Level Requis', value=search[0].get('require_lvl'), inline=False)
                newEmbed.add_field(name='Créateur', value=search[0].get('author'), inline=False)
                total = int(search[0].get('require_lvl')) + 1
                dispo = (total - len(search[0].get('user')))
                participant = []
                if len(search[0].get('user')):
                    for u in search[0].get('user'):
                        print(u['name'])
                        participant.append(u['name'])
                    participant = ','.join(participant)
                else:
                    participant = 'none'
                newEmbed.add_field(name='Place disponible', value='{}/{}'.format(str(dispo), str(total)), inline=False)
                newEmbed.add_field(name='Participant', value=participant, inline=False)

                await message.edit(embed=newEmbed)

bot.run(Token)
