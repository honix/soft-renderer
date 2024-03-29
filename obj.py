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
                indices = phrases[1:]
                length = len(indices)

                def add_polygon(a, b, c):
                    p1 = int(indices[a].split('/')[0]) - 1
                    p2 = int(indices[b].split('/')[0]) - 1
                    p3 = int(indices[c].split('/')[0]) - 1
                    polygons.append(Polygon([p1, p2, p3]))

                # TODO: algoritmize
                if length == 3:
                    add_polygon(0, 1, 2)
                elif length == 4:
                    add_polygon(0, 1, 2)
                    add_polygon(0, 2, 3)
                elif length == 5:
                    add_polygon(0, 1, 2)
                    add_polygon(0, 2, 3)
                    add_polygon(0, 3, 4)
                elif length == 6:
                    add_polygon(0, 1, 2)
                    add_polygon(0, 2, 3)
                    add_polygon(0, 3, 4)
                    add_polygon(0, 4, 5)
            
    return Mesh(vertices, polygons)
