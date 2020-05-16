import pygame, sys, math, numpy
import src.input as input
import src.matrix as matrix
import src.vector as vector
from src.vector import Vec3
from src.mesh import *
from src.camera import Camera
from src.renderer import Renderer

meshCube = [
    # SOUTH
    Triangle(Vec3(0.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 0.0)),
    Triangle(Vec3(0.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 0.0, 0.0)),

    # EAST                                                      
    Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0)),
    Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 0.0, 1.0)),

    # NORTH                                                     
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(1.0, 1.0, 1.0), Vec3(0.0, 1.0, 1.0)),
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 0.0, 1.0)),

    # WEST                                                      
    Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 1.0, 0.0)),
    Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 0.0)),

    # TOP                                                       
    Triangle(Vec3(0.0, 1.0, 0.0), Vec3(0.0, 1.0, 1.0), Vec3(1.0, 1.0, 1.0)),
    Triangle(Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 1.0, 0.0)),

    # BOTTOM                                                    
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0)),
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), Vec3(1.0, 0.0, 0.0)),
]

def move_camera(camera, dtime):
    # Camera dir
    m = pygame.mouse.get_rel()
    camera.pitch += -m[1] * 0.01
    camera.yaw += -m[0] * 0.01
    
    xz = math.cos(camera.pitch)
    r = math.radians(90)
    forward = Vec3(xz * math.sin(camera.yaw), math.sin(camera.pitch), xz * math.cos(-camera.yaw))
    left = Vec3(xz * math.sin(camera.yaw + r), 0, xz * math.cos(-camera.yaw - r))
    right = Vec3(xz * math.sin(camera.yaw - r), 0, xz * math.cos(-camera.yaw + r))

    # Camera pos
    move = Vec3()

    if input.is_down("up"):
        move += forward

    if input.is_down("down"):
        move -= forward

    if input.is_down("left"):
        move += left

    if input.is_down("right"):
        move += right

    if input.is_down("shift"):
        move.y -= 1

    if input.is_down("space"):
        move.y += 1

    speed = 5 * dtime
    cpos = camera.get_pos()
    camera.set_pos(cpos + (move * speed))


class Game:
    def __init__(self):
        self.camera = Camera()
        self.camera.set_pos(Vec3(0, 0, -4))
        # self.camera.set_dir(Vec3(0, 1, 1))
        self.renderer = Renderer()
        self.theta = 0
        # self.mesh = Mesh("assets/teapot.obj")
        self.mesh = Mesh("assets/axis.obj")
        # self.mesh = Mesh()
        # self.mesh.tris = meshCube

        pygame.mouse.set_visible(False)
        pygame.event.set_grab(True)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if input.is_down("esc"):
                pygame.quit()
                sys.exit()

            dtime = self.renderer.clock.tick(60) / 1000.0

            move_camera(self.camera, dtime)

            # Frame updating
            self.renderer.clear()
            # self.theta += 1
            # self.renderer.draw(self.camera, self.mesh, vector.apply(Vec3(self.theta, self.theta, self.theta), math.radians))
            # self.renderer.draw(self.camera, self.mesh, vector.apply(Vec3(160, self.theta, 0), math.radians))
            self.renderer.draw(self.camera, self.mesh, vector.apply(Vec3(0, 0, 0), math.radians))

            pygame.display.flip()

if __name__ == "__main__":
    Game().start()
