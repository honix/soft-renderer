from PIL import Image
import numpy as np

from ..geometry.point import Point

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

    def downsample(self, n):
        # Box filter: average each n x n block of samples into one pixel.
        h, w = self.height // n, self.width // n
        data = self.data.reshape(h, n, w, n, -1).mean(axis=(1, 3))
        buf = Buffer(w, h, channels=data.shape[-1])
        buf.data[:] = np.round(data).astype(np.uint8)
        return buf

    def show(self, mode='RGB'):
        img = Image.fromarray(self.data, mode)
        img.show()

    def save(self, path, mode='RGB'):
        Image.fromarray(self.data, mode).save(path)
