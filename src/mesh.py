from .vector import Vec3

class UV:
    def __init__(self, u = 0, v = 0, w = 0):
        self.u = float(u)
        self.v = float(v)
        self.w = float(w)

class Triangle:
    def __init__(self, v1 = None, v2 = None, v3 = None, uv1 = None, uv2 = None, uv3 = None, textureIndex = 0):
        self.verts = []
        if v1 and v2 and v3:
            self.verts = [v1, v2, v3]

        if uv1 and uv2 and uv3:
            self.uv = [uv1, uv2, uv3]
        else:
            self.uv = [UV(0, 0, 0), UV(0, 0, 0), UV(0, 0, 0)]

        self.normal = Vec3()
        self.color = (255, 255, 255)
        self.index = textureIndex

class Mesh:
    def __init__(self, file=""):
        self.tris = []
        if file != "":
            self.fromFile(file)

    def fromFile(self, path):
        f = open(path, "r")
        lines = f.readlines()

        verts = []
        tris = []

        for line in lines:
            l = line.split()
            if line[0] == "v":
                verts.append(Vec3(float(l[1]), float(l[2]), float(l[3])))

            if line[0] == "f":
                tris.append(Triangle(
                    verts[int(l[1]) - 1],
                    verts[int(l[2]) - 1],
                    verts[int(l[3]) - 1]
                ))

        self.tris = tris

def Cube():
    mesh = Mesh()
    mesh.tris = [
        # SOUTH
        Triangle(Vec3(0.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 0),
        Triangle(Vec3(0.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 0),

        # EAST
        Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 1),
        Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 0.0, 1.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 1),

        # NORTH
        Triangle(Vec3(1.0, 0.0, 1.0), Vec3(1.0, 1.0, 1.0), Vec3(0.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 2),
        Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 0.0, 1.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 2),

        # WEST
        Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 1.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 3),
        Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 3),

        # TOP
        Triangle(Vec3(0.0, 1.0, 0.0), Vec3(0.0, 1.0, 1.0), Vec3(1.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 4),
        Triangle(Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 1.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 4),

        # BOTTOM
        Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 5),
        Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), Vec3(1.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 5),
    ]
    return mesh
