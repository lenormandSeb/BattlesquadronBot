class ModuleGame:
    def __init__(self):
        self.weapon = [
            'Canon Faible',
            'Canon',
            'Laser',
            'Batterie Multiple',
            'Double Laser',
            'Barrage',
            'Lance-missile Dart'
        ]

    def findWeapon(self, moduleName):
        print(moduleName)

class Cruiser(ModuleGame):
    id_user = ''
    user_name = ''
    ship_name = ''
    ship_module = []

    def __init__(self, user, ship):
        self.id_user = user.id
        self.user_name = user.name
        self.ship_name = ship
    
    def jsonify(self):
        """ Return dictonnary """
        ship = {
            'id_user' : self.id_user,
            'user' : self.user_name,
            'ship_name' : self.ship_name,
            'module' : self.ship_module
        }
        return ship
