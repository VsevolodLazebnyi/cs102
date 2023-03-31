import random
import typing as tp

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(self, width: int = 640, height: int = 480, cell_size: int = 10, speed: int = 10) -> None:
        self.width = width
        self.height = height
        self.cell_size = cell_size

        # Устанавливаем размер окна
        self.screen_size = width, height
        # Создание нового окна
        self.screen = pygame.display.set_mode(self.screen_size)

        # Вычисляем количество ячеек по вертикали и горизонтали
        self.cell_width = self.width // self.cell_size
        self.cell_height = self.height // self.cell_size

        # Скорость протекания игры
        self.speed = speed

    def draw_lines(self) -> None:
        for x in range(0, self.width, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (x, 0), (x, self.height))
        for y in range(0, self.height, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color("black"), (0, y), (self.width, y))

    def run(self) -> None:
        """Запустить игру"""
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption("Game of Life")
        self.screen.fill(pygame.Color("white"))

        # Создание списка клеток
        self.grid = self.create_grid(randomize=True)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            # Отрисовка списка клеток
            # Выполнение одного шага игры (обновление состояния ячеек)
            self.draw_grid()
            self.draw_lines()
            self.grid = self.get_next_generation()

            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()

    def create_grid(self, randomize: bool = False) -> Grid:
        grid = [[0 for _ in range(self.cell_height)] for _ in range(self.cell_width)]
        if randomize:
            for i in range(self.cell_width):
                for j in range(self.cell_height):
                    grid[i][j] = random.randint(0, 1)
        return grid

    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                pygame.draw.rect(
                    self.screen,
                    pygame.Color("green") if self.grid[i][j] == 1 else pygame.Color("white"),
                    (
                        i * self.cell_size,
                        j * self.cell_size,
                        self.cell_size,
                        self.cell_size,
                    ),
                )

    def get_neighbours(self, cell: Cell) -> Cells:
        neighbours = []
        # qwerty
        for i in range(-1, 2):
            for j in range(-1, 2):
                if cell[0] + i >= 0 and cell[1] + j >= 0 and not (i == 0 and j == 0):
                    # Не является самой собой и не выходит за пределы сетки
                    try:
                        neighbours.append(self.grid[cell[0] + i][cell[1] + j])
                        # Сбор по индексам
                    except IndexError:
                        pass
        return neighbours

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.

        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        new_grid = [[0 for _ in range(self.cell_height)] for _ in range(self.cell_width)]
        for i in range(self.cell_width):
            for j in range(self.cell_height):
                cell = (i, j)
                n_neighbors = sum(self.get_neighbours(cell))
                if self.grid[i][j]:
                    if n_neighbors == 2 or n_neighbors == 3:
                        new_grid[i][j] = 1
                else:
                    if n_neighbors == 3:
                        new_grid[i][j] = 1
        return new_grid
