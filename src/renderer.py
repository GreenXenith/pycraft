import pygame, math, numpy
from . import matrix, vector
from .vector import Vec3
from .mesh import Triangle

class Renderer:
    def __init__(self, screen_w = 800, screen_h = 600):
        pygame.init()
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = pygame.display.set_mode((screen_w, screen_h))
        self.clock = pygame.time.Clock()

        self.matProj = matrix.perspective(screen_h / screen_w, 90.0, 0.1, 1000.0)

    def clear(self):
        self.screen.fill((0, 0, 0))

    def draw(self, camera, mesh, rotation): #, position):
        # Rotation matricies
        matRotZ = matrix.rotateZ(rotation.z)
        matRotY = matrix.rotateY(rotation.y)
        matRotX = matrix.rotateX(rotation.x)

        # Translation matrix (will convert to func later)
        matTran = numpy.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1],
        ])

        # World matrix
        matWorld = matrix.identity()
        matWorld = numpy.dot(matWorld, matRotX)
        matWorld = numpy.dot(matWorld, matRotY)
        matWorld = numpy.dot(matWorld, matRotZ)
        matWorld = numpy.dot(matTran, matWorld)

        # Camera matrix
        up = Vec3(0, 1, 0)
        target = camera.pos + camera.dir

        matCamera = matrix.pointAt(camera.pos, target, up)
        matView = matrix.inversePointAt(matCamera) # Invert pointAt matrix

        rasterTris = []
        for tri in mesh.tris:
            # Transform triangle
            transformedTri = Triangle()
            for point in tri.verts:
                transformedPoint = numpy.dot(vector.toMatrix(point), matWorld)
                transformedTri.verts.append(vector.fromMatrix(transformedPoint))

            # Normal calculation
            line1 = transformedTri.verts[1] - transformedTri.verts[0]
            line2 = transformedTri.verts[2] - transformedTri.verts[0]

            normal = vector.cross(line1, line2).normalize()
            camRay = transformedTri.verts[0] - camera.pos

            # Culling
            if vector.dot(normal, camRay) > 0.0:
                points = []
                for point in transformedTri.verts:
                    viewPoint = numpy.dot(vector.toMatrix(point), matView)
                    # viewPoint = vector.toMatrix(point)

                    # Perspective Projection
                    projPoint = numpy.dot(viewPoint, self.matProj)
                    p = vector.fromMatrix(projPoint)

                    if p.z != 0:
                        p.x /= p.z
                        p.y /= p.z

                    # Scale to screen
                    p.x += 1.0
                    p.y += 1.0
                    p.x *= 0.5 * self.screen_w
                    p.y *= 0.5 * self.screen_h
                    p.y = self.screen_h - p.y

                    points.append(p)

                projectedTri = Triangle(*points)
                projectedTri.normal = normal
                rasterTris.append(projectedTri)

        # Poor-man's depth buffer
        sortedTries = sorted(rasterTris, key = lambda tri: (tri.verts[0].z + tri.verts[1].z + tri.verts[2].z) / 3.0)

        # Light direction
        light = Vec3(-1, -1, -1).normalize()

        for tri in sortedTries:
            # Calcuate triangle lighting
            dlight = 255 * max(0.1, vector.dot(light, tri.normal))

            points = []
            for v in tri.verts:
                points.append((v.x, v.y))

            # pygame.draw.lines(self.screen, (255, 255, 255), True, points)
            pygame.draw.polygon(self.screen, (dlight, dlight, dlight), points)
