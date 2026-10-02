from .point import Point

class Vertex:
    def __init__(self, position, normal=None):
        self.position = position
        self.tposition = position
        self.clip = None  # clip-space x, y, z, w, before the perspective divide
        self.w = 1  # clip-space w, kept for perspective-correct interpolation

        self.normal = normal

        self.color = None
        self.uv = None

    def lerp(self, other, t):
        v = Vertex(
            Point.lerp(self.position, other.position, t),
            Point.lerp(self.normal, other.normal, t)
        )
        v.tposition = Point.lerp(self.tposition, other.tposition, t)
        return v