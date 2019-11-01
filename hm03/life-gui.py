import pygame
from pygame.locals import *

from life import GameOfLife
from ui import UI


class GUI(UI):

    def __init__(self, life: GameOfLife, cell_size: int=10, speed: int=10) -> None:
        super().__init__(GameOfLife)
        self.cell_size = cell_size
        self.screen_size = self.cell_size, self.cell_size
        self.screen = pygame.display.set_mode(self.screen_size)
        # Предыдущее поколение клеток
        self.prev_generation = GameOfLife.create_grid(self)
        # Текущее поколение клеток
        self.curr_generation = GameOfLife.create_grid(randomize=randomize)

    def draw_lines(self) -> None:
        """ Отрисовать сетку """
        for x in range(0, self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (x, 0), (x, self.cell_size))
        for y in range(0, self.cell_size, self.cell_size):
            pygame.draw.line(self.screen, pygame.Color('black'),
                    (0, y), (self.cell_size, y))


    def draw_grid(self) -> None:
        """
        Отрисовка списка клеток с закрашиванием их в соответствующе цвета.
        """
        y = 0
        grid = GameOfLife.create_grid(self, True)

        for i in grid:
            x = 0
            for v in i:
                color = 'white' if v == 0 else 'green'
                pygame.draw.rect(self.screen, pygame.Color(color),
                                    pygame.Rect(x, y, self.cell_size, self.cell_size))
                x += self.cell_size
            y += self.cell_size


    def run(self) -> None:
        """ Запустить игру """
        pygame.init()
        clock = pygame.time.Clock()
        pygame.display.set_caption('Game of Life')

        self.screen.fill(pygame.Color('white'))
        # Создание списка клеток
        self.life.step()


        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
            self.draw_lines()
            # Отрисовка списка клеток
            self.draw_grid()
            # Выполнение одного шага игры (обновление состояния ячеек)
            GameOfLife.get_next_generation(self)
            pygame.display.flip()
            clock.tick(self.speed)
        pygame.quit()



game = GUI([10, 10], True)

game.run()