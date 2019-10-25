grid = []

with open('grid.txt', 'r') as file:
    for i in file:
        grid.append(i[:-1])

print(grid)