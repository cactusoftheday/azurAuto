class enemy:
    def __init__(self, distance,coords):
        self.reachable = True
        self.distance = distance
        self.coords = coords
    def setReachable(self):
        self.reachable = False