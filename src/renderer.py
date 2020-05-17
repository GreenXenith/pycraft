import pygame, math, numpy
from . import matrix, vector
from .vector import Vec3
from .mesh import Triangle

def planeLineIntersection(plane_p, normal, lineStart, lineEnd):
    normal = normal.normalize()
    d = -vector.dot(normal, plane_p)
    ad = vector.dot(lineStart, normal)
    bd = vector.dot(lineEnd, normal)
    t = (-d - ad) / (bd - ad)
    line = lineEnd - lineStart
    return lineStart + (line * t)

def clipTriangle(planeP, normal, triangle):
    normal = normal.normalize()

    insidePoints = []
    outsidePoints = []

    for p in triangle.verts:
        dist = (normal.x * p.x + normal.y * p.y + normal.z * p.z - vector.dot(normal, planeP))
        if dist >= 0:
            insidePoints.append(p)
        else:
            outsidePoints.append(p)

    inside = len(insidePoints)
    outside = len(outsidePoints)

    if inside == 0:
        return []
    elif inside == 1 and outside == 2:
        tri = Triangle()
        tri.color = triangle.color
        tri.normal = triangle.normal

        tri.verts.append(insidePoints[0])
        tri.verts.append(planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[0]))
        tri.verts.append(planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[1]))

        return [tri]
    elif inside == 2 and outside == 1:
        tri1 = Triangle()
        tri1.color = triangle.color
        tri1.normal = triangle.normal

        tri2 = Triangle()
        tri2.color = triangle.color
        tri2.normal = triangle.normal

        tri1.verts.append(insidePoints[0])
        tri1.verts.append(insidePoints[1])
        tri1.verts.append(planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[0]))

        tri2.verts.append(insidePoints[1])
        tri2.verts.append(tri1.verts[2])
        tri2.verts.append(planeLineIntersection(planeP, normal, insidePoints[1], outsidePoints[0]))

        return [tri1, tri2]
    else: # inside == 3
        return [triangle]

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
        matWorld = numpy.dot(matWorld, matRotZ)
        matWorld = numpy.dot(matWorld, matRotY)
        matWorld = numpy.dot(matWorld, matRotX)
        matWorld = numpy.dot(matTran, matWorld)

        # Camera matrix
        up = Vec3(0, 1, 0)
        target = Vec3(0, 0, 1)

        matCamRot = matrix.identity()
        matCamRot = numpy.dot(matCamRot, matrix.rotateY(camera.yaw))
        matCamRot = numpy.dot(matCamRot, matrix.rotateX(camera.pitch))

        lookDir = numpy.dot(matCamRot, vector.toMatrix(target))
        target = camera.pos + vector.fromMatrix(lookDir)

        matCamera = matrix.pointAt(camera.pos, target, up)
        matView = matrix.inversePointAt(matCamera)

        rasterTris = []
        for tri in mesh.tris:
            # Transform triangle
            transformedTri = Triangle()
            for point in tri.verts:
                transformedPoint = numpy.dot(matWorld, vector.toMatrix(point))
                transformedTri.verts.append(vector.fromMatrix(transformedPoint))

            # Normal calculation
            line1 = transformedTri.verts[1] - transformedTri.verts[0]
            line2 = transformedTri.verts[2] - transformedTri.verts[0]

            normal = vector.cross(line1, line2).normalize()
            camRay = transformedTri.verts[0] - camera.pos

            # Culling
            if vector.dot(normal, camRay) < 0.0:
                viewPoints = []
                for point in transformedTri.verts:
                    viewPoint = numpy.dot(vector.toMatrix(point), matView)
                    viewPoints.append(vector.fromMatrix(viewPoint))

                # Clip on near z plane
                clippedTris = clipTriangle(Vec3(0.0, 0.0, 0.11), Vec3(0.0, 0.0, 1.0), Triangle(*viewPoints))
                for clipTri in clippedTris:
                    projPoints = []
                    for clipPoint in clipTri.verts:
                        # Perspective Projection
                        projPoint = numpy.dot(vector.toMatrix(clipPoint), self.matProj)
                        p = vector.fromMatrix(projPoint)

                        if p.z != 0:
                            p.x /= p.z
                            p.y /= p.z

                        # Scale to screen
                        p.x += 1.0
                        p.y += 1.0
                        p.x *= 0.5 * self.screen_w
                        p.y *= 0.5 * self.screen_h
                        p.x = self.screen_w - p.x
                        p.y = self.screen_h - p.y

                        projPoints.append(p)

                    projectedTri = Triangle(*projPoints)
                    projectedTri.normal = normal
                    rasterTris.append(projectedTri)

        # Poor-man's depth buffer
        sortedTris = sorted(rasterTris, key = lambda tri: (tri.verts[0].z + tri.verts[1].z + tri.verts[2].z) / 3.0, reverse = True)

        # Light direction
        light = Vec3(0, 1, -1).normalize()

        for tri in sortedTris:
            # Clip triangles on screen edges
            clippedTris = [tri]
            for p in range(4):
                for _ in range(len(clippedTris)):
                    test = clippedTris.pop(0)

                    newTris = []

                    if p == 0:
                        newTris = clipTriangle(Vec3(0.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), test)
                    elif p == 1:
                        newTris = clipTriangle(Vec3(0.0, self.screen_h - 1, 0.0), Vec3(0.0, -1.0, 0.0), test)
                    elif p == 2:
                        newTris = clipTriangle(Vec3(0.0, 0.0, 0.0), Vec3(1.0, 0.0, 0.0), test)
                    elif p == 3:
                        newTris = clipTriangle(Vec3(self.screen_w - 1, 0.0, 0.0), Vec3(-1.0, 0.0, 0.0), test)

                    for t in newTris:
                        clippedTris.append(t)

            for tri in clippedTris:
                # Calcuate triangle lighting
                dlight = 255 * max(0.1, vector.dot(light, tri.normal))

                points = []
                for v in tri.verts:
                    points.append((v.x, v.y))

                pygame.draw.polygon(self.screen, (dlight, dlight, dlight), points)
                # pygame.draw.lines(self.screen, (0, 0, 0), True, points)
