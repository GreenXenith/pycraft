"""
Unit tests
"""

def spec(description, callable):
    if callable(): # Returns bool
        print("PASSED: " + description)
    else:
        print("FAILED: " + description)

if __name__ == "__main__":
    import math

    # vector.py
    print("\nvector.py:")
    import src.vector as vector
    from src.vector import Vec3

    v1 = Vec3(0, 1, 2)
    spec("Vec3(x, y, z)", lambda: v1.x == 0 and v1.y == 1 and v1.z == 2)
    spec("Vec3(x, y)", lambda: Vec3(0, 1) == Vec3(0, 1, 0))
    spec("Vec3(x)", lambda: Vec3(0) == Vec3(0, 0, 0))

    spec("print(Vec3)", lambda: Vec3(3, 2, 1).__repr__() == "Vector {x: 3.0, y: 2.0, z: 1.0}")

    spec("Vec3 == Vec3", lambda: (Vec3(0, 0, 0) == Vec3(0)) == True)
    spec("Vec3 == Vec3", lambda: (Vec3(0, 0, 0) == Vec3(1)) == False)
    spec("Vec3 != Vec3", lambda: (Vec3(0, 0, 0) != Vec3(1)) == True)
    spec("Vec3 != Vec3", lambda: (Vec3(0, 0, 0) != Vec3(0)) == False)

    v1 = Vec3(1, 2, 3)
    v2 = Vec3(3, 2, 1)

    spec("Vec3 + Vec3", lambda: v1 + v2 == Vec3(4))
    spec("Vec3 - Vec3", lambda: v1 - v2 == Vec3(-2, 0, 2))
    spec("Vec3 / Vec3", lambda: v1 / v2 == Vec3(1 / 3, 2 / 2, 3 / 1))
    spec("Vec3 * Vec3", lambda: v1 * v2 == Vec3(3, 4, 3))

    spec("round(Vec3)", lambda: round(Vec3(0.3, 0.5, 0.7)) == Vec3(0, 0, 1))
    spec("math.floor(Vec3)", lambda: math.floor(Vec3(0.3, 0.5, 0.7)) == Vec3(0, 0, 0))
    spec("math.ceil(Vec3)", lambda: math.ceil(Vec3(0.3, 0.5, 0.7)) == Vec3(1, 1, 1))

    spec("Vec3.length()", lambda: Vec3(1, 1, 0).length() == math.sqrt(2))
    spec("Vec3.normalize()", lambda: Vec3(3, 4, 0).normalize() == Vec3(0.6, 0.8, 0.0))

    spec("vector.new()", lambda: vector.new(0) == Vec3(0))
    spec("vector.new()", lambda: vector.new(1, 2, 3) == Vec3(1, 2, 3))

    spec("vector.apply()", lambda: vector.apply(Vec3(4, 16, 64), math.sqrt) == Vec3(2, 4, 8))

    spec("vector.distance()", lambda: vector.distance(Vec3(0), Vec3(1, 1, 0)) == math.sqrt(2))

    v1 = vector.apply(vector.direction(Vec3(0), Vec3(1)), lambda v: round(v, 10))
    v2 = vector.apply(Vec3(math.sqrt(2)).normalize(), lambda v: round(v, 10))
    spec("vector.direction()", lambda: v1 == v2)
    spec("vector.angle()", lambda: vector.angle(Vec3(0, 1, 0), Vec3(0, 0, 1)) == math.radians(90))

    spec("vector.dot()", lambda: vector.dot(Vec3(1, 2, 3), Vec3(4, 5, 6)) == 32)
    spec("vector.cross()", lambda: vector.cross(Vec3(1, 2, 3), Vec3(4, 5, 6)) == Vec3(-3, 6, -3))


    # camera.py
    print("\ncamera.py:")
    from src.camera import Camera

    cam = Camera()

    spec("Camera()", lambda: cam.pos == Vec3(0))

    cam.set_pos(Vec3(1))
    spec("Camera.set_pos()", lambda: cam.pos == Vec3(1))
    spec("Camera.get_pos()", lambda: cam.get_pos() == Vec3(1))


    # mesh.py
    print("\nmesh.py:")
    from src.mesh import *

    uv = UV()
    spec("UV()", lambda: uv.u == 0 and uv.v == 0 and uv.w == 0)

    uv = UV(0, 0.5, 1)
    spec("UV(u, v, w)", lambda: uv.u == 0 and uv.v == 0.5 and uv.w == 1)

    tri = Triangle()
    spec("Triangle()", lambda: tri.uv[0].u == 0 and tri.verts == [] and tri.normal == Vec3() \
                               and tri.color == (255, 255, 255) and tri.index == 0)

    tri = Triangle(Vec3(0), Vec3(1), Vec3(2), UV(0, 0, 1), UV(1, 0, 1), UV(0, 1, 1), 2)
    spec("Triangle(v1, v2, v3, uv1, uv2, uv3, i)", lambda: \
                               tri.uv[0].w == 1 and tri.verts == [Vec3(0), Vec3(1), Vec3(2)] \
                               and tri.normal == Vec3() and tri.color == (255, 255, 255) and tri.index == 2)

    mesh = Mesh()
    spec("Mesh()", lambda: mesh.tris == [])

    cube = Cube()
    spec("Cube()", lambda: cube.tris[0].verts[0] == Vec3(0) and cube.tris[11].verts[2] == Vec3(1, 0, 0))


    # map.py
    print("\nmap.py:")
    from src.map import Map

    def findInMap(m, find):
        c = 0
        for x in m.map:
            for z in x:
                for y in z:
                    if y == find:
                        c += 1
        return c

    m = Map(0)
    spec("Map(0)", lambda: findInMap(m, 1) == 0)

    m = Map(16)
    spec("Map(16)", lambda: findInMap(m, 1) == 16 * 16)

    m = Map(16, True)
    spec("Map(16, True)", lambda: findInMap(m, 1) == 4)
