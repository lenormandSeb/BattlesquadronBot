import json
class User:
    id_user = ''
    name = ''
    RS = ''
    BS = ''
    WS = ''

    def __init__(self, user):
        self.id_user = user.id
        self.name = user.name
    
    def updateRedStar(self, value):
        self.RS = value
        return

    def jsonify(self):
        user = {
            "id_user" :self.id_user,
            "name":self.name,
            "RS":self.RS
        }
        return user
