from PIL import Image
import numpy as np

from point import Point

class Buffer:
    def __init__(self, width, height, channels, fill_value=0, dtype=np.uint8):
        self.width = width
        self.height = height
        self.data = np.full(
            (height, width, channels) if channels > 1 else (height, width), 
            fill_value=fill_value, 
            dtype=dtype
        )

    def __setitem__(self, key, item):
        self.data[key] = item 

    def __getitem__(self, key):
        return self.data[key]

    def show(self, mode='RGB'):
        img = Image.fromarray(self.data, mode)
        img.show()
