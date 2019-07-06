import math

class P:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + 
                         math.pow(self.y - other.y, 2))
