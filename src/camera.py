import numpy
from .vector import Vec3

class Camera:
    def __init__(self):
        self.pos = Vec3(0, 0, 0)
        self.fov = 90
        self.yaw = 0
        self.pitch = 0

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_fov(self, angle):
        self.fov = angle

    def get_fov(self):
        return self.fov
