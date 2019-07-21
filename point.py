import math

# TODO: name it Point or Vector? Vector can be used for side definition
class Point:
    def __init__(self, x, y, z = 0):
        # TODO: use numpy vector for speed
        self.x = x
        self.y = y
        self.z = z

    def integrated(self):
        return Point(
            int(self.x),
            int(self.y),
            int(self.z),
        )

    # TODO: arifmetic ops

    def distance(self, other):
        return math.sqrt(math.pow(self.x - other.x, 2) + 
                         math.pow(self.y - other.y, 2))

