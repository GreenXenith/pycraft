import numpy
from .vector import Vec3

class Camera:
    def __init__(self):
        self.pos = Vec3(0, 0, 0)
        self.dir = Vec3(0, 0, 1)
        self.fov = 90

    def set_pos(self, pos):
        self.pos = pos

    def get_pos(self):
        return self.pos

    def set_dir(self, dir):
        self.dir = dir

    def get_dir(self):
        return self.dir

    def set_fov(self, angle):
        self.fov = angle

    def get_fov(self):
        return self.fov
