import curses
import time

from life import GameOfLife
from ui import UI


class Console(UI):
    def __init__(self, life: GameOfLife) -> None:
        super().__init__(life)
        self.life = life
        self.screen = (self.life.rows, self.life.cols)


    def draw_borders(self, screen) -> None:
        """ Отобразить рамку. """

        screen_ = curses.initscr()
        curses.curs_set(0)

        screen_.addstr(0, 0, f'+{"-" * screen[1]}+')

        for i in range(screen[0]):
            screen_.addstr(i+1, 0, '|')
            screen_.addstr(i+1, screen[1] + 1, '|')

        screen_.addstr(screen[0] + 1, 0, f'+{"-" * screen[1]}+')

        curses.endwin()


    def draw_grid(self, screen) -> None:
        """ Отобразить состояние клеток. """
        screen_ = curses.initscr()

        row = 0
        for i in screen:
            my_str = ''
            col = 1
            for v in i:
                if v == 1:
                    my_str += f'Ж'
                else:
                    my_str += f' '

                col += 1
            row += 1
            screen_.addstr(row, 1, my_str)

        curses.endwin()


    def run(self) -> None:
        screen = curses.initscr()
        stop = True

        while stop:
            if not self.life.is_changing:
                stop = False

            self.draw_borders(self.screen)
            self.draw_grid(self.life.curr_generation)
            self.life.step()
            screen.refresh()
            time.sleep(1)

            if self.life.is_max_generations_exceed:
                stop = False

        curses.endwin()

