import numpy as np
import math
from utils import lerp

class Point(np.ndarray):
    def __new__(cls, x=0, y=0, z=0):
        return np.asarray([x, y, z]).view(cls)

    @property
    def xyz(self): return self[:3]

    @property
    def x(self): return self[0]

    @x.setter
    def x(self, v): self[0] = v    
        
    @property
    def y(self): return self[1]

    @y.setter
    def y(self, v): self[1] = v    
        
    @property
    def z(self): return self[2]

    @z.setter
    def z(self, v): self[2] = v

    def lerp(self, other, t):
        return Point(
            lerp(self.x, other.x, t),
            lerp(self.y, other.y, t),
            lerp(self.z, other.z, t),
        )

    def integrated(self):
        return self.astype(np.int).view(Point)

    def to_list(self):
        return [self.x, self.y, self.z]

    