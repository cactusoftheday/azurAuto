class fleet:
    def __init__(self, oilCost, fleetName):
        self.ammo = 5
        self.oilCost = oilCost
        self.fleetName = fleetName

    def useAmmo(self):
        self.ammo = self.ammo - 1

