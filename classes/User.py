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
    
    def updateResearch(self, index, i):
        if index == 0:
            self.updateRedStar(i)
        elif index == 1:
            self.updateBlueStar(i)
        elif index == 2:
            self.updateWhiteStar(i)
        else:
            return 'something wrong'
    
    def updateRedStar(self, value):
        self.RS = value
        return
    
    def updateBlueStar(self, value):
        self.BS = value
        return
    
    def updateWhiteStar(self, value):
        self.WS = value
        return
    
    def jsonify(self):
        user = {
            "id_user" :self.id_user,
            "name":self.name,
            "RS":self.RS, 
            "BS":self.BS, 
            "WS":self.WS, 
        }
        return user
