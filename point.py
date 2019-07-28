import numpy as np
from utils import lerp

class Point:
    def __init__(self, x=0, y=0, z=0):
        self.x = x
        self.y = y
        self.z = z

    @classmethod
    def from_numpy(cls, array):
        return cls(array.item(0), array.item(1), array.item(2))

    @staticmethod
    def lerp(a, b, t):
        return Point(
            lerp(a.x, b.x, t),
            lerp(a.y, b.y, t),
            lerp(a.z, b.z, t),
        )

    def integrated(self):
        return Point(
            int(self.x),
            int(self.y),
            int(self.z),         
        )

    def to_list(self):
        return [self.x, self.y, self.z]

    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z

    def __neg__(self):
        return Point(
            -self.x,
            -self.y,
            -self.z,
        )

    def __sub__(self, other):
        return Point(
            self.x - other.x,
            self.y - other.y,
            self.z - other.z,
        )