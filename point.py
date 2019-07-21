import numpy as np

class Point:
    def __init__(self, x, y, z = 0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_numpy(cls, array):
        return cls(array.item(0), array.item(1), array.item(2))

    def integrated(self):
        return Point(
            int(self.x),
            int(self.y),
            int(self.z),         
        )