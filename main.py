import math, numpy, pygame, sys, time
import src.input as input
import src.matrix as matrix
import src.vector as vector
from src.vector import Vec3
from src.mesh import Cube
from src.camera import Camera
from src.renderer import Renderer
from src.map import Map

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

        self.screen_w = screen_w
        self.screen_h = screen_h

        self.visible = False
        self.esc = False
        pygame.mouse.set_visible(self.visible)
        pygame.event.set_grab(not self.visible)
        pygame.mouse.set_pos((screen_w / 2, screen_h / 2))

        self.camera = Camera()
        self.camera.set_pos(Vec3(0, 0, -32))

        self.renderer = Renderer(screen_w, screen_h)

        # Only generate cube mesh once
        self.cube = Cube()

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

        self.map = Map(8, False) # Change False to True for testing mode

    def start(self):
        while True:
            begin = time.time()

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

            m = self.map.map
            for x in range(len(m)):
                for z in range(len(m[x])):
                    for y in range(len(m[x][z])):
                        if m[x][z][y] == 1:
                            self.renderer.draw(self.camera, self.cube, Vec3(x, y, z), Vec3(0, 0, 0), self.texture)

            self.renderer.update()

            mid_w = self.screen_w / 2
            mid_h = self.screen_h / 2
            pygame.draw.line(self.renderer.screen, (255, 255, 255), (mid_w, mid_h + 10), (mid_w, mid_h - 10))
            pygame.draw.line(self.renderer.screen, (255, 255, 255), (mid_w + 10, mid_h), (mid_w - 10, mid_h))

            pygame.display.flip() # Double flip to show crosshair

            pygame.display.set_caption(str(round(1.0 / (time.time() - begin), 1)) + "FPS")

if __name__ == "__main__":
    Game().start()
