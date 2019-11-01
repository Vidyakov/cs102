import pathlib
import random
# TODO: Не сделал проверку на максимальное количество поколений и на смену поколений.

from typing import List, Optional, Tuple

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

        matrix = [[0] * self.rows for _ in range(self.cols)]

        if randomize == False:
            return matrix
        else:
            row = 0
            for i in matrix:
                col = 0
                for _ in i:
                    matrix[row][col] = random.randint(0, 1)
                    col += 1
                row += 1
            return matrix


    def get_neighbours(self, cell: Cell) -> Cells:
        grid = self.curr_generation
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
        grid = self.curr_generation
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


        return new_matrix


    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = self.curr_generation
        self.curr_generation = self.get_next_generation()
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
        until_grid = self.prev_generation
        after_grid = self.curr_generation

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
        """
        Прочитать состояние клеток из указанного файла.
        """
        matrix = []

        with open(filename, 'r') as file:
            for i in file:
                matrix.append(i[:-1])

        new_matrix = list(map(list, matrix))

        last_matrix = []
        for i in new_matrix:
            last_matrix.append(list(map(int, i)))


        game_return = GameOfLife([len(last_matrix[0]), len(last_matrix)])
        game_return.curr_generation = last_matrix

        return game_return


    def save(self, filename):
        """
        Сохранить текущее состояние клеток в указанный файл.
        """
        some = 0
        grid = self.curr_generation
        with open(filename, 'w') as file:
            for i in grid:
                score = 0
                for v in i:
                    if score == 0 and some > 0:
                        print(f'\n{v}', file=file, end='')
                    else:
                        print(v, file=file, end='')
                        some += 1
                    score += 1

