import numpy as np
import matrix_functions
import pygame
from numba import njit


@njit(fastmath=True)
def any_func(arr, a, b):
    return np.any((arr == a) | (arr == b))


class Object3D:
    def __init__(self, render, vertexes, faces):
        self.render = render
        self.vertices = np.array([np.array(v) for v in vertexes])
        self.faces = np.array([np.array(f) for f in faces])

        self.color_faces = [(pygame.Color("orange"), face) for face in self.faces]
        self.movement_flag, self.draw_vertexes = True, True
        self.font = pygame.font.SysFont('Arial', 30, bold=True)
        self.label = ''

    def draw(self):
        self.screen_projection()
        self.movement()

    def movement(self):
        if self.movement_flag:
            self.rotate_y(pygame.time.get_ticks() % 0.005)

    def screen_projection(self):
        vertexes = self.vertices @ self.render.camera.camera_matrix()
        vertexes = vertexes @ self.render.projection.projection_matrix
        vertexes /= vertexes[:, -1].reshape(-1, 1)
        vertexes[(vertexes > 2) | (vertexes < -2)] = 0
        vertexes = vertexes @ self.render.projection.to_screen_matrix
        vertexes = vertexes[:, :2]

        for index, color_face in enumerate(self.color_faces):
            color, face = color_face
            polygon = vertexes[face]
            if not any_func(polygon, self.render.H_WIDTH, self.render.H_HEIGHT):
                pygame.draw.polygon(self.render.screen, color, polygon, 1)
                if self.label:
                    text = self.font.render(self.label[index], True, pygame.Color("white"))
                    self.render.screen.blit(text, polygon[-1])

        if self.draw_vertexes:
            for vertexes in vertexes:
                if not any_func(vertexes, self.render.H_WIDTH, self.render.H_HEIGHT):
                    pygame.draw.circle(self.render.screen, pygame.Color("white"), vertexes, 2)

    def translate(self, pos):
        self.vertices = self.vertices @ matrix_functions.translate(pos)

    def scale(self, scale_to):
        self.vertices = self.vertices @ matrix_functions.scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ matrix_functions.rotate_x(angle)

    def rotate_y(self, angle):
        self.vertices = self.vertices @ matrix_functions.rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ matrix_functions.rotate_z(angle)

class Axes(Object3D):
    def __init__(self, render):
        super().__init__(render)
        self.vertices = np.array(
            [
                [0, 0, 0, 1],
                [1, 0, 0, 1],
                [0, 1, 0, 1],
                [0, 0, 1, 1]
            ]
        )

        self.faces = np.array(
            [
                (0, 1),
                (0, 2),
                (0, 3)
            ]
        )

        self.colors = [pygame.Color("red"), pygame.Color("green"), pygame.Color("blue")]
        self.color_faces = [(color, face) for color, face in zip(self.colors, self.faces)]

        self.draw_vertexes = False
        self.label = 'XYZ'
