import pygame, math, numpy, copy
from . import matrix, vector
from .vector import Vec3
from .mesh import Triangle, UV

def planeLineIntersection(plane_p, normal, lineStart, lineEnd):
    normal = normal.normalize()
    d = -vector.dot(normal, plane_p)
    ad = vector.dot(lineStart, normal)
    bd = vector.dot(lineEnd, normal)
    t = (-d - ad) / (bd - ad)
    line = lineEnd - lineStart
    return lineStart + (line * t), t

def clipTriangle(planeP, normal, triangle):
    normal = normal.normalize()

    insidePoints = []
    outsidePoints = []
    insideTex = []
    outsideTex = []

    for i in range(len(triangle.verts)):
        p = triangle.verts[i]
        dist = (normal.x * p.x + normal.y * p.y + normal.z * p.z - vector.dot(normal, planeP))
        if dist >= 0:
            insidePoints.append(p)
            insideTex.append(triangle.uv[i])
        else:
            outsidePoints.append(p)
            outsideTex.append(triangle.uv[i])

    nInsidePoints = len(insidePoints)
    nOutsidePoints = len(outsidePoints)

    if nInsidePoints == 0:
        return []
    elif nInsidePoints == 1 and nOutsidePoints == 2:
        tri = Triangle()
        tri.color = triangle.color
        tri.normal = triangle.normal
        tri.index = triangle.index

        tri.verts.append(insidePoints[0])
        tri.uv[0] = copy.deepcopy(insideTex[0])

        v, t = planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[0])
        tri.verts.append(v)
        tri.uv[1].u = t * (outsideTex[0].u - insideTex[0].u) + insideTex[0].u
        tri.uv[1].v = t * (outsideTex[0].v - insideTex[0].v) + insideTex[0].v
        tri.uv[1].w = t * (outsideTex[0].w - insideTex[0].w) + insideTex[0].w

        v, t = planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[1])
        tri.verts.append(v)
        tri.uv[2].u = t * (outsideTex[1].u - insideTex[0].u) + insideTex[0].u
        tri.uv[2].v = t * (outsideTex[1].v - insideTex[0].v) + insideTex[0].v
        tri.uv[2].w = t * (outsideTex[1].w - insideTex[0].w) + insideTex[0].w

        return [tri]
    elif nInsidePoints == 2 and nOutsidePoints == 1:
        tri1 = Triangle()
        tri1.color = triangle.color
        tri1.normal = triangle.normal
        tri1.index = triangle.index

        tri2 = Triangle()
        tri2.color = triangle.color
        tri2.normal = triangle.normal
        tri2.index = triangle.index

        tri1.verts.append(insidePoints[0])
        tri1.verts.append(insidePoints[1])
        tri1.uv[0] = insideTex[0]
        tri1.uv[1] = insideTex[1]

        v, t = planeLineIntersection(planeP, normal, insidePoints[0], outsidePoints[0])
        tri1.verts.append(v)
        tri1.uv[2].u = t * (outsideTex[0].u - insideTex[0].u) + insideTex[0].u
        tri1.uv[2].v = t * (outsideTex[0].v - insideTex[0].v) + insideTex[0].v
        tri1.uv[2].w = t * (outsideTex[0].w - insideTex[0].w) + insideTex[0].w

        tri2.verts.append(insidePoints[1])
        tri2.verts.append(tri1.verts[2])
        tri2.uv[0] = insideTex[1]
        tri2.uv[1] = copy.deepcopy(tri1.uv[2])

        v, t = planeLineIntersection(planeP, normal, insidePoints[1], outsidePoints[0])
        tri2.verts.append(v)
        tri2.uv[2].u = t * (outsideTex[0].u - insideTex[1].u) + insideTex[1].u
        tri2.uv[2].v = t * (outsideTex[0].v - insideTex[1].v) + insideTex[1].v
        tri2.uv[2].w = t * (outsideTex[0].w - insideTex[1].w) + insideTex[1].w

        return [tri1, tri2]
    else: # nInsidePoints == 3
        return [triangle]

def lightColor(rgb, light):
    c = lambda v: max(0, min(int(v * light), 255))
    return int("%02x%02x%02x" % (c(rgb[0]), c(rgb[1]), c(rgb[2])), 16)

def drawTexturedTriangle(pixelBuffer, depthBuffer, triangle, texture, light):
    verts = [[triangle.verts[0], triangle.uv[0]], [triangle.verts[1], triangle.uv[1]], [triangle.verts[2], triangle.uv[2]]]
    s = sorted(verts, key = lambda s: s[0].y)

    x1 = int(s[0][0].x); y1 = int(s[0][0].y); u1 = s[0][1].u; v1 = s[0][1].v; w1 = s[0][1].w
    x2 = int(s[1][0].x); y2 = int(s[1][0].y); u2 = s[1][1].u; v2 = s[1][1].v; w2 = s[1][1].w
    x3 = int(s[2][0].x); y3 = int(s[2][0].y); u3 = s[2][1].u; v3 = s[2][1].v; w3 = s[2][1].w

    dy1 = y2 - y1
    dx1 = x2 - x1
    dv1 = v2 - v1
    du1 = u2 - u1
    dw1 = w2 - w1

    dy2 = y3 - y1
    dx2 = x3 - x1
    dv2 = v3 - v1
    du2 = u3 - u1
    dw2 = w3 - w1

    dax_step = 0.0; dbx_step = 0.0
    du1_step = 0.0; dv1_step = 0.0
    du2_step = 0.0; dv2_step = 0.0
    dw1_step = 0.0; dw2_step = 0.0

    if dy1 != 0: dax_step = dx1 / abs(dy1)
    if dy2 != 0: dbx_step = dx2 / abs(dy2)

    if dy1 != 0: du1_step = du1 / abs(dy1)
    if dy1 != 0: dv1_step = dv1 / abs(dy1)
    if dy1 != 0: dw1_step = dw1 / abs(dy1)

    if dy2 != 0: du2_step = du2 / abs(dy2)
    if dy2 != 0: dv2_step = dv2 / abs(dy2)
    if dy2 != 0: dw2_step = dw2 / abs(dy2)

    if dy1 != 0:
        for i in range(y1, y2 + 1):
            ax = x1 + int((i - y1) * dax_step)
            bx = x1 + int((i - y1) * dbx_step)

            tex_su = u1 + (i - y1) * du1_step
            tex_sv = v1 + (i - y1) * dv1_step
            tex_sw = w1 + (i - y1) * dw1_step

            tex_eu = u1 + (i - y1) * du2_step
            tex_ev = v1 + (i - y1) * dv2_step
            tex_ew = w1 + (i - y1) * dw2_step

            if ax > bx:
                tempx = ax
                temp_su = tex_su
                temp_sv = tex_sv
                temp_sw = tex_sw

                ax = bx
                tex_su = tex_eu
                tex_sv = tex_ev
                tex_sw = tex_ew

                bx = tempx
                tex_eu = temp_su
                tex_ev = temp_sv
                tex_ew = temp_sw

            tex_u = tex_su
            tex_v = tex_sv
            tex_w = tex_sw

            tstep = 1.0
            if ax != bx:
                tstep = 1.0 / (bx - ax)
            t = 0.0

            for j in range(ax, bx):
                tex_u = (1.0 - t) * tex_su + t * tex_eu
                tex_v = (1.0 - t) * tex_sv + t * tex_ev
                tex_w = (1.0 - t) * tex_sw + t * tex_ew

                if tex_w != 0:
                    tex_u /= tex_w
                    tex_v /= tex_w

                t_x = max(0, min(int(math.floor(16 * (tex_u))), 15))
                t_y = max(0, min(int(math.floor(16 * (tex_v))), 15))

                if tex_w > depthBuffer[j][i]:
                    pixelBuffer[j][i] = lightColor(texture.get_at((t_x, t_y)), light)
                    depthBuffer[j][i] = tex_w

                t += tstep

    dy1 = y3 - y2
    dx1 = x3 - x2
    dv1 = v3 - v2
    du1 = u3 - u2
    dw1 = w3 - w2

    if dy1 != 0: dax_step = dx1 / abs(dy1)
    if dy2 != 0: dbx_step = dx2 / abs(dy2)

    du1_step = 0; dv1_step = 0
    if dy1 != 0: du1_step = du1 / abs(dy1)
    if dy1 != 0: dv1_step = dv1 / abs(dy1)
    if dy1 != 0: dw1_step = dw1 / abs(dy1)

    if dy1 != 0:
        for i in range(y2, y3 + 1):
            ax = x2 + int((i - y2) * dax_step)
            bx = x1 + int((i - y1) * dbx_step)

            tex_su = u2 + (i - y2) * du1_step
            tex_sv = v2 + (i - y2) * dv1_step
            tex_sw = w2 + (i - y2) * dw1_step

            tex_eu = u1 + (i - y1) * du2_step
            tex_ev = v1 + (i - y1) * dv2_step
            tex_ew = w1 + (i - y1) * dw2_step

            if ax > bx:
                tempx = ax
                temp_su = tex_su
                temp_sv = tex_sv
                temp_sw = tex_sw

                ax = bx
                tex_su = tex_eu
                tex_sv = tex_ev
                tex_sw = tex_ew

                bx = tempx
                tex_eu = temp_su
                tex_ev = temp_sv
                tex_ew = temp_sw

            tex_u = tex_su
            tex_v = tex_sv
            tex_w = tex_sw

            tstep = 1.0
            if ax != bx:
                tstep = 1.0 / (bx - ax)
            t = 0.0

            for j in range(ax, bx):
                tex_u = (1.0 - t) * tex_su + t * tex_eu
                tex_v = (1.0 - t) * tex_sv + t * tex_ev
                tex_w = (1.0 - t) * tex_sw + t * tex_ew

                if tex_w != 0:
                    tex_u /= tex_w
                    tex_v /= tex_w

                t_x = max(0, min(int(math.floor(16 * (tex_u))), 15))
                t_y = max(0, min(int(math.floor(16 * (tex_v))), 15))

                if tex_w > depthBuffer[j][i]:
                    pixelBuffer[j][i] = lightColor(texture.get_at((t_x, t_y)), light)
                    depthBuffer[j][i] = tex_w

                t += tstep

    return

class Renderer:
    def __init__(self, screen_w = 800, screen_h = 600):
        self.screen_w = screen_w
        self.screen_h = screen_h
        self.screen = pygame.display.set_mode((screen_w, screen_h))

        self.pixelBuffer = numpy.zeros((screen_w, screen_h))
        self.depthBuffer = numpy.zeros((screen_w, screen_h))

        self.clock = pygame.time.Clock()
        pygame.mouse.get_rel()

        self.matProj = matrix.perspective(screen_h / screen_w, 90.0, 0.1, 1000.0)

    def clear(self):
        self.screen.fill((0, 0, 0))
        self.pixelBuffer = numpy.zeros((self.screen_w, self.screen_h))
        self.depthBuffer = numpy.zeros((self.screen_w, self.screen_h))

    def update(self):
        pygame.surfarray.blit_array(self.screen, self.pixelBuffer)
        pygame.display.flip()

    def draw(self, camera, mesh, position, rotation, textures = ["", "", "", "", "", ""]):
        # Rotation matricies
        matRotZ = matrix.rotateZ(rotation.z)
        matRotY = matrix.rotateY(rotation.y)
        matRotX = matrix.rotateX(rotation.x)

        # Translation matrix
        matTran = numpy.array([
            [1, 0, 0, position.x],
            [0, 1, 0, position.y],
            [0, 0, 1, position.z],
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
                # View transform
                viewedTriangle = Triangle()
                for point in transformedTri.verts:
                    viewPoint = numpy.dot(vector.toMatrix(point), matView)
                    viewedTriangle.verts.append(vector.fromMatrix(viewPoint))
                    viewedTriangle.uv = copy.deepcopy(tri.uv)

                # Clip on near z plane
                clippedTris = clipTriangle(Vec3(0.0, 0.0, 0.11), Vec3(0.0, 0.0, 1.0), viewedTriangle)
                for clippedTri in clippedTris:
                    projectedTri = Triangle()
                    projectedTri.normal = normal
                    projectedTri.index = tri.index

                    for i in range(3):
                        # Perspective Projection
                        projPoint = numpy.dot(vector.toMatrix(clippedTri.verts[i]), self.matProj)
                        p = vector.fromMatrix(projPoint)
                        w = projPoint[3]

                        if w != 0:
                            projectedTri.uv[i].u = clippedTri.uv[i].u / w
                            projectedTri.uv[i].v = clippedTri.uv[i].v / w
                            projectedTri.uv[i].w = 1.0 / w
                            p /= w

                        # Scale to screen
                        p.x += 1.0
                        p.y += 1.0
                        p.x *= 0.5 * self.screen_w
                        p.y *= 0.5 * self.screen_h
                        p.x = self.screen_w - p.x
                        p.y = self.screen_h - p.y

                        projectedTri.verts.append(p)

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

                    clippedTris.extend(newTris)

            for tri in clippedTris:
                # Calcuate triangle lighting
                tLight = max(0.1, vector.dot(light, tri.normal))
                drawTexturedTriangle(self.pixelBuffer, self.depthBuffer, tri, textures[tri.index], tLight)

                # points = []
                # for v in tri.verts:
                #     points.append((v.x, v.y))
                # pygame.draw.polygon(self.screen, (dlight, dlight, dlight), points)
                # pygame.draw.lines(self.screen, (255, 255, 255), True, points)
