import math, numpy
from . import vector
from .vector import Vec3

def identity():
    matIdent = numpy.zeros((4, 4))
    matIdent[0][0] = 1.0
    matIdent[1][1] = 1.0
    matIdent[2][2] = 1.0
    matIdent[3][3] = 1.0

    return matIdent

def rotateX(theta):
    matRotX = numpy.zeros((4, 4))
    matRotX[0][0] = 1.0
    matRotX[1][1] = math.cos(theta)
    matRotX[1][2] = math.sin(theta)
    matRotX[2][1] = -math.sin(theta)
    matRotX[2][2] = math.cos(theta)
    matRotX[3][3] = 1.0

    return matRotX

def rotateY(theta):
    matRotY = numpy.zeros((4, 4))
    matRotY[0][0] = math.cos(theta)
    matRotY[0][2] = math.sin(theta)
    matRotY[2][0] = -math.sin(theta)
    matRotY[1][1] = 1.0
    matRotY[2][2] = math.cos(theta)
    matRotY[3][3] = 1.0

    return matRotY

def rotateZ(theta):
    matRotZ = numpy.zeros((4, 4))
    matRotZ[0][0] = math.cos(theta)
    matRotZ[0][1] = math.sin(theta)
    matRotZ[1][0] = -math.sin(theta)
    matRotZ[1][1] = math.cos(theta)
    matRotZ[2][2] = 1.0
    matRotZ[3][3] = 1.0

    return matRotZ

def pointAt(pos, target, up):
    newForward = (target - pos).normalize()

    a = newForward * vector.dot(up, newForward)
    newUp = (up - a).normalize()

    newRight = vector.cross(newUp, newForward)

    matPointAt = numpy.zeros((4, 4))
    matPointAt[0][0] = newRight.x;   matPointAt[0][1] = newRight.y;   matPointAt[0][2] = newRight.z;   matPointAt[0][3] = 0.0
    matPointAt[1][0] = newUp.x;      matPointAt[1][1] = newUp.y;      matPointAt[1][2] = newUp.z;      matPointAt[1][3] = 0.0
    matPointAt[2][0] = newForward.x; matPointAt[2][1] = newForward.y; matPointAt[2][2] = newForward.z; matPointAt[2][3] = 0.0
    matPointAt[3][0] = pos.x;        matPointAt[3][1] = pos.y;        matPointAt[3][2] = pos.z;        matPointAt[3][3] = 1.0

    return matPointAt

def inversePointAt(matrix):
    matInv = numpy.zeros((4, 4))
    matInv[0][0] = matrix[0][0]; matInv[0][1] = matrix[1][0]; matInv[0][2] = matrix[2][0]; matInv[0][3] = 0.0
    matInv[1][0] = matrix[0][1]; matInv[1][1] = matrix[1][1]; matInv[1][2] = matrix[2][1]; matInv[1][3] = 0.0
    matInv[2][0] = matrix[0][2]; matInv[2][1] = matrix[1][2]; matInv[2][2] = matrix[2][2]; matInv[2][3] = 0.0
    matInv[3][0] = -(matrix[3][0] * matInv[0][0] + matrix[3][1] * matInv[1][0] + matrix[3][2] * matInv[2][0])
    matInv[3][1] = -(matrix[3][0] * matInv[0][1] + matrix[3][1] * matInv[1][1] + matrix[3][2] * matInv[2][1])
    matInv[3][2] = -(matrix[3][0] * matInv[0][2] + matrix[3][1] * matInv[1][2] + matrix[3][2] * matInv[2][2])
    matInv[3][3] = 1.0
    return matrix

def perspective(ratio, fov, near, far):
    fovRad = 1.0 / math.tan(fov * 0.5 / 180.0 * math.pi)

    matPersp = numpy.zeros((4, 4))
    matPersp[0][0] = ratio * fovRad
    matPersp[1][1] = fovRad
    matPersp[2][2] = far / (far - near)
    matPersp[3][2] = (-far * near) / (far - near)
    matPersp[2][3] = 1.0
    matPersp[3][3] = 0.0

    return matPersp
