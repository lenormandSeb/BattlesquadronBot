import os
import json
from tinydb import TinyDB, Query
from dotenv import load_dotenv
import discord

load_dotenv()
db = TinyDB(os.getenv('PATH_BDD') + 'bdd/user_database.json')
table = db.table('eventRs')
QueryDB = Query()
redStar = 'https://cdn.discordapp.com/attachments/691684927309348937/696077525562032188/redStar.png'

class Star():
    __slot__ = ('message', 'author', 'require_lvl', 'hour', 'users')
    
    def __init__(self, **kwargs):
        try:
            self.id_event = kwargs.get('message')
            author = kwargs.get('author')
            self.author_id = author.id
            self.author = author.name
            try:
                self.hour = kwargs.get('hour')
            except:
                pass
            self.require_lvl = kwargs.get('require_lvl')
            if int(self.require_lvl) >= 4:
                total = 4
            else:
                total = int(self.require_lvl) + 1
            self.place = str(total)
            self.users = kwargs.get('users')
            self.annulation = False
        except:
            pass

    def getEvent(self, id_event):
        return table.search(QueryDB.id_event == id_event)

    def update(self, reaction, message, userUpdate, update):
        isPresent = False
        event = self.getEvent(reaction.message_id)
        users = event[0].get('users')
        if reaction.emoji.name == '🔴' and reaction.user_id == userUpdate.id:
            return True
        if update == True:
            for user in users:
                if user['name'] == reaction.member.name:
                    isPresent = True
            if not isPresent:
                if not userUpdate.name in users :
                    total = int(event[0].get('require_lvl')) + 1
                    dispo = (total - len(event[0].get('users')))
                    if dispo > 0:
                        newUser = {
                            'name' : userUpdate.name
                        }
                        event[0].get('users').append(newUser)
            else:
                return False
        else:
            if reaction.user_id != event[0].get('author_id'):
                finduser = {'name' : userUpdate.name}
                if finduser in event[0].get('users') :
                    toRemove = {
                        'name' : userUpdate.name
                    }
                    event[0].get('users').remove(toRemove)
                else:
                    return False
            else:
                return False

        update = {
            'id_event':event[0].get('id_event'),
            'users': event[0].get('users')
        }

        table.upsert(update, QueryDB.id_event == reaction.message_id)
        return True

    def create_red_star(self):
        id_event = self.id_event
        table.upsert(self.__to_Json(), QueryDB.id_event == id_event)

    def getEmbed(self):
        embed = discord.Embed(
            title='Création de Rs'
        )
        if self.annulation:
            embed.add_field(name='Annulation', value='Cette RS a été annuler', inline=False)
            return embed

        embed.set_thumbnail(url=redStar)
        embed.add_field(name='Niveau Requis', value=self.require_lvl, inline=False)
        embed.add_field(name='Créateur', value=self.author, inline=False)
        if self.hour:
            embed.add_field(name='Heure de début', value=self.hour, inline=False)
        total = int(self.place)
        dispo = (total - len(self.users))
        participant = []
        for u in self.users:
            participant.append(u['name'])
        embed.add_field(name='Place disponible', value='{}/{}'.format(str(dispo), self.place), inline=False)
        embed.add_field(name='Participant', value=','.join(participant), inline=False)
        embed.add_field(name='-------', value='Pour particper, appuie sur 👍', inline=False)

        return embed

    def updateEmbed(self,reaction):
        event = self.getEvent(reaction.message_id)
        if reaction.emoji.name == '🔴':
            self.annulation = True
            return self.getEmbed()
        self.annulation = False
        self.require_lvl = event[0].get('require_lvl')
        self.author = event[0].get('author')
        self.hour = event[0].get('hour') if event[0].get('hour') else None
        self.place = event[0].get('place')
        self.users = event[0].get('users')

        return self.getEmbed()

    def __to_Json(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__))
