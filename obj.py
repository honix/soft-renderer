from mesh import Mesh
from point import Point
from vertex import Vertex
from polygon import Polygon

def read_obj(path):
    vertices = []
    polygons = []

    with open(path) as file:
        for line in file:
            line = line.strip()
            if len(line) < 1: continue
            if line[0] == '#': continue

            phrases = line.split()
            head = phrases[0]

            if head == 'v':
                x = float(phrases[1])
                y = float(phrases[2])
                z = float(phrases[3])
                vertices.append(Vertex(Point(x, y, z)))
            elif head == 'f':
                p1 = int(phrases[1]) - 1
                p2 = int(phrases[2]) - 1
                p3 = int(phrases[3]) - 1
                polygons.append(Polygon([p1, p2, p3]))
            
    return Mesh(vertices, polygons)
