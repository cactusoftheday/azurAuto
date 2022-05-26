class fleet:
    def __init__(self, fleetName):
        self.ammo = 5
        self.fleetName = fleetName

    def useAmmo(self):
        self.ammo = self.ammo - 1

