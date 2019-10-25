import pathlib
import random

from typing import List, Optional, Tuple
from pprint import pprint as pp

Cell = Tuple[int, int]
Cells = List[int]
Grid = List[Cells]


class GameOfLife:
    def __init__(self, size=[10, 10], randomize: bool=True, max_generations: Optional[float]=float('inf')) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1


    def create_grid(self, randomize: bool=False) -> Grid:

        self.matrix = [[0] * self.rows for _ in range(self.cols)] # self.rows and self.cols <- не проходит

        if randomize == False:
            return self.matrix
        else:
            row = 0
            for i in self.matrix:
                col = 0
                for _ in i:
                    self.matrix[row][col] = random.randint(0, 1)
                    col += 1
                row += 1
            return self.matrix


    def get_neighbours(self, cell: Cell) -> Cells:
        grid = self.matrix
        relative_neighbours = [[-1, -1], [0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0]]
        list_of_neighbors = []

        for i in relative_neighbours:
            i[0] += cell[0]
            i[1] += cell[1]

        for i in relative_neighbours:
            row, col = i
            try:
                if row >= 0 and col >= 0:
                    list_of_neighbors.append(grid[col][row])
                else:
                    continue
            except IndexError:
                continue

        return list_of_neighbors


    def get_next_generation(self) -> Grid:
        grid = self.matrix
        new_matrix = [[0] * self.rows for _ in range(self.cols)]
        total = {}

        y = 0
        for i in grid:
            x = 0
            for _ in i:
                neighbours = self.get_neighbours((x, y))
                score = 0
                for m in neighbours:
                    score += 1 if m == 1 else 0
                total[(y, x)] = score
                x += 1
            y += 1

        for i in total:
            row, col = i
            if total[(row, col)] == 3:
                new_matrix[row][col] = 1
            elif total[(row, col)] == 2:
                new_matrix[row][col] = 1 if grid[row][col] == 1 else 0
            else:
                new_matrix[row][col] = 0

        self.matrix = new_matrix
        return self.matrix


    def step(self) -> None:
        # TODO: Проверить на ликвидность
        """
        Выполнить один шаг игры.
        """
        self.create_grid(True)
        self.get_next_generation()
        self.generations += 1


    @property
    def is_max_generations_exceeded(self):
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        max_generations = self.max_generations
        if max_generations > self.generations:
            return True
        else:
            return False


    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        until_grid = self.matrix
        after_grid = self.get_next_generation()

        col = 0
        for i in until_grid:
            row = 0
            for v in i:
                if v != after_grid[col][row]:
                    return True
                row += 1
            col += 1

        return False



    @staticmethod
    def from_file(filename: pathlib.Path) -> 'GameOfLife':
        # TODO: Дописать return к функции
        """
        Прочитать состояние клеток из указанного файла.
        """
        matrix = []

        with open(filename, 'r') as file:
            for i in file:
                matrix.append(i[:-1])


    def save(self, filename):
        # TODO: Правильно ли я их записал? self.generations?
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        grid = self.matrix
        with open(filename, 'w') as file:
            for i in range(1, self.generations):
                print(dict(i, grid), file=file)





life = GameOfLife((5, 5))
life.save('steps_exam.txt')
