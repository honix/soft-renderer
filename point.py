import math

class Point:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    def integrate(self):
        self.x = int(self.x)
        self.y = int(self.y)
        self.z = int(self.z)

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + 
                         math.pow(self.y - other.y, 2))

