import math, numpy

class Vec3:
    def __init__(self, x = 0, y = None, z = None):
        if y == None: y = x
        if z == None: z = x
        self.x = float(x)
        self.y = float(y)
        self.z = float(z)

    def __repr__(self):
        return "Vector {{x: {0}, y: {1}, z: {2}}}".format(self.x, self.y, self.z)

    def __eq__(self, b):
        return self.x == b.x and self.y == b.y and self.z == b.z

    def __ne__(self, b):
        return self.x != b.x or self.y != b.y or self.z != b.z

    def __add__(self, b):
        if isinstance(b, (int, float)): b = Vec3(b)
        return Vec3(self.x + b.x, self.y + b.y, self.z + b.z)

    def __sub__(self, b):
        if isinstance(b, (int, float)): b = Vec3(b)
        return Vec3(self.x - b.x, self.y - b.y, self.z - b.z)

    def __mul__(self, b):
        if isinstance(b, (int, float)): b = Vec3(b)
        return Vec3(self.x * b.x, self.y * b.y, self.z * b.z)

    def __truediv__(self, b):
        if isinstance(b, (int, float)): b = Vec3(b)
        return Vec3(self.x / b.x, self.y / b.y, self.z / b.z)

    def __round__(self):
        return apply(self, round)

    def __floor__(self):
        return apply(self, math.floor)

    def __ceil__(self):
        return apply(self, math.ceil)

    def length(self):
        return math.hypot(self.x, math.hypot(self.y, self.z))

    def normalize(self):
        l = self.length()
        if l == 0:
            return Vec3(0)
        else:
            return self / l

def new(*args):
    return Vec3(*args)

def apply(v, func):
    return Vec3(func(v.x), func(v.y), func(v.z))

def distance(a, b):
    x = a.x - b.x
    y = a.y - b.y
    z = a.z - b.z
    return math.hypot(x, math.hypot(y, z))

def direction(pos1, pos2):
    return Vec3(pos2.x - pos1.x, pos2.y - pos1.y, pos2.z - pos1.z).normalize()

def angle(a, b):
    return math.atan2(cross(a, b).length(), dot(a, b))

def dot(a, b):
    return a.x * b.x + a.y * b.y + a.z * b.z

def cross(a, b):
    x = a.y * b.z - a.z * b.y
    y = a.z * b.x - a.x * b.z
    z = a.x * b.y - a.y * b.x
    return Vec3(x, y, z)

def toMatrix(v):
    return numpy.array([v.x, v.y, v.z, 1.0])

def fromMatrix(m):
    return Vec3(m[0], m[1], m[2])
