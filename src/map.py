import numpy
from .noise import perlin

class Map:
    def __init__(self, size, testing = False):
        self.map = numpy.zeros((size, size, size))
        if testing:
            #        x  z  y
            self.map[0][0][0] = 1
            self.map[1][0][0] = 1
            self.map[0][1][0] = 1
            self.map[1][1][0] = 1
        else:
            p = perlin((size, size), (1, 1))
            for x in range(len(p)):
                for z in range(len(p[x])):
                    y = int(p[x][z] * 4)
                    self.map[x][z][y] = 1
