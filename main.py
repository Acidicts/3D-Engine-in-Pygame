import pygame
from object_3d import *
from camera import *
from projection import *

model = "untitled.obj"

class SoftwareRender:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Software Render")
        self.RES = self.WIDTH, self.HEIGHT = 1280, 720
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 60
        self.screen = pygame.display.set_mode(self.RES)
        self.clock = pygame.time.Clock()

        self.object = None
        self.camera = None
        self.projection = None
        self.axes = None
        self.world_axes = None

        self.create_objects()

    def create_objects(self):
        self.camera = Camera(self, (-5, 5, -50))
        self.projection = Projection(self)
        self.object = self.get_object_from_file('models/' + "untitled.obj")

    def get_object_from_file(self, filename):
        vertex, faces = [], []
        with open(filename) as f:
            for line in f:
                if line.startswith('v '):
                    vertex.append([float(i) for i in line.split()[1:]] + [1])
                elif line.startswith('f'):
                    faces_ = line.split()[1:]
                    faces.append([int(face_.split('/')[0]) - 1 for face_ in faces_])

        return Object3D(self, vertex, faces)

    def draw(self):
        self.screen.fill(pygame.Color("darkslategray"))
        self.object.draw()
        self.screen.convert_alpha()

    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pygame.event.get() if i.type == pygame.QUIT]
            pygame.display.set_caption(f"Software Render | FPS: {self.clock.get_fps()}")
            pygame.display.flip()
            self.clock.tick(self.FPS)


if __name__ == "__main__":
    app = SoftwareRender()
    app.run()
