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
    px = 0
    py = 0
    pz = 0

    speed = 5 * dtime

    if input.is_down("up"):
        pz += speed

    if input.is_down("down"):
        pz += -speed

    if input.is_down("left"):
        px += -speed

    if input.is_down("right"):
        px += speed

    if input.is_down("shift"):
        py += -speed

    if input.is_down("space"):
        py += speed

    cpos = camera.get_pos()
    camera.set_pos(cpos + Vec3(px, py, pz))

    m = pygame.mouse.get_rel()
    # cdir = camera.get_dir()
    cdir = vector.toMatrix(camera.get_dir())

    rotX = matrix.rotateX(math.radians(-m[1] * 0.5))
    rotY = matrix.rotateY(math.radians(-m[0] * 0.5))

    cdir = numpy.dot(cdir, rotY)
    cdir = numpy.dot(cdir, rotX)

    # pitch = math.radians(-m[1])
    # yaw = math.radians(-m[0])
    # xz = math.cos(pitch)

    # rot = Vec3(xz * math.cos(yaw), math.sin(pitch), xz * math.sin(-yaw))
    # print(rot)

    # camera.set_dir((cdir + rot).normalize())
    # camera.set_dir(vector.fromMatrix(cdir))

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

        # pygame.mouse.set_visible(False)
        # pygame.event.set_grab(True)

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
