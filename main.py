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
    Triangle(Vec3(0.0, 0.0, 0.0), Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 0),
    Triangle(Vec3(0.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 0),

    # EAST
    Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 1),
    Triangle(Vec3(1.0, 0.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 0.0, 1.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 1),

    # NORTH
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(1.0, 1.0, 1.0), Vec3(0.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 2),
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 0.0, 1.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 2),

    # WEST
    Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 1.0), Vec3(0.0, 1.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 3),
    Triangle(Vec3(0.0, 0.0, 1.0), Vec3(0.0, 1.0, 0.0), Vec3(0.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 3),

    # TOP
    Triangle(Vec3(0.0, 1.0, 0.0), Vec3(0.0, 1.0, 1.0), Vec3(1.0, 1.0, 1.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 4),
    Triangle(Vec3(0.0, 1.0, 0.0), Vec3(1.0, 1.0, 1.0), Vec3(1.0, 1.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 4),

    # BOTTOM
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), UV(0, 1, 1), UV(0, 0, 1), UV(1, 0, 1), 5),
    Triangle(Vec3(1.0, 0.0, 1.0), Vec3(0.0, 0.0, 0.0), Vec3(1.0, 0.0, 0.0), UV(0, 1, 1), UV(1, 0, 1), UV(1, 1, 1), 5),
]

def update_camera(camera, dtime):
    rn = math.radians(90) # Ninety degrees in radians
    ro = math.radians(1) # One degree in radians

    # Camera dir
    m = pygame.mouse.get_rel()
    camera.pitch = max(-rn + ro, min(camera.pitch - m[1] * 0.01, rn - ro))
    camera.yaw += -m[0] * 0.01

    xz = 1 # math.cos(camera.pitch) # Uncomment for pitch-fly
    forward = Vec3(xz * math.sin(camera.yaw), 0, xz * math.cos(-camera.yaw))
    left = Vec3(xz * math.sin(camera.yaw + rn), 0, xz * math.cos(-camera.yaw - rn))
    right = Vec3(xz * math.sin(camera.yaw - rn), 0, xz * math.cos(-camera.yaw + rn))

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
    def __init__(self, screen_w = 800, screen_h = 600):
        pygame.init()

        self.visible = False
        self.esc = False
        pygame.mouse.set_visible(self.visible)
        pygame.event.set_grab(not self.visible)
        pygame.mouse.set_pos((screen_w / 2, screen_h / 2))

        self.camera = Camera()
        self.camera.set_pos(Vec3(0, 0, -4))
        # self.camera.set_dir(Vec3(0, 1, 1))
        self.renderer = Renderer(screen_w, screen_h)
        self.theta = 0
        # self.mesh = Mesh("media/teapot.obj")
        # self.mesh = Mesh("media/axis.obj")
        self.mesh = Mesh()
        self.mesh.tris = meshCube
        self.media = {
            "grass_block_side": pygame.image.load("media/grass_block_side.png"),
            "grass": pygame.image.load("media/grass.png"),
            "dirt": pygame.image.load("media/dirt.png")
        }
        self.texture = [
            self.media["grass_block_side"],
            self.media["grass_block_side"],
            self.media["grass_block_side"],
            self.media["grass_block_side"],
            self.media["grass"],
            self.media["dirt"]
        ]

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            if not self.esc and input.is_down("esc"):
                self.visible = not self.visible

                pygame.mouse.set_visible(self.visible)
                pygame.event.set_grab(not self.visible)

                if self.visible: # Center cursor
                    pygame.mouse.set_pos((self.renderer.screen_w / 2, self.renderer.screen_h / 2))
                else: # Reset cursor
                    pygame.mouse.get_rel()

            self.esc = input.is_down("esc")

            dtime = self.renderer.clock.tick(60) / 1000.0

            if not self.visible:
                update_camera(self.camera, dtime)

            # Frame updating
            self.renderer.clear()
            # self.theta += 1
            # self.renderer.draw(self.camera, self.mesh, Vec3(0, 0, 0), vector.apply(Vec3(self.theta, self.theta, self.theta), math.radians), self.texture)
            # self.renderer.draw(self.camera, self.mesh, Vec3(0, 0, 0), vector.apply(Vec3(160, self.theta, 0), math.radians))
            self.renderer.draw(self.camera, self.mesh, Vec3(0, 0, 0), Vec3(0, 0, 0), self.texture)

            pygame.display.flip()

if __name__ == "__main__":
    Game().start()
