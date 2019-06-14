import mazes
import random

r = random.randint(0,2)
mazze = mazes.mazes[r].copy()
Found = False
Path = []


def search(lvl, x, y, _path=[]):
    level = lvl.copy()
    level[y][x] = 8
    path = _path.copy()
    path.append((y, x))
    global Found
    global Path
    if Found == False:

        # left
        if level[y][x - 1] == 1:
            search(lvl, x - 1, y, path)
        if level[y][x - 1] == 9:
            print("Found")
            path.append((y, x - 1))

            Path = path
            Found = True
            return

        # right
        if level[y][x + 1] == 1:
            search(lvl, x + 1, y, path)
        if level[y][x + 1] == 9:
            print("Found")
            path.append((y, x + 1))

            Path = path
            Found = True
            return

        # up
        if level[y - 1][x] == 1:
            search(lvl, x, y - 1, path)
        if level[y - 1][x] == 9:
            print("Found")
            path.append((y - 1, x))

            Path = path
            Found = True
            return

        # down
        if level[y + 1][x] == 1:
            search(lvl, x, y + 1, path)
        if level[y + 1][x] == 9:
            print("Found")

            path.append((y + 1, x))

            Path = path
            Found = True
            return
