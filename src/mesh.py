from .vector import Vec3

class UV:
    def __init__(self, u = 0, v = 0, w = 0):
        self.u = float(u)
        self.v = float(v)
        self.w = float(w)

class Triangle:
    def __init__(self, v1 = None, v2 = None, v3 = None, uv1 = UV(0, 0, 0), uv2 = UV(0, 0, 0), uv3 = UV(0, 0, 0), textureIndex = 0):
        self.verts = []
        if v1 and v2 and v3:
            self.verts = [v1, v2, v3]

        self.uv = [uv1, uv2, uv3]
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
