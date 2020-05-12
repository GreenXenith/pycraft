from .vector import Vec3

class Triangle:
    def __init__(self, *verts):
        self.verts = list(verts)
        self.normal = Vec3()
        self.color = (255, 255, 255)

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
