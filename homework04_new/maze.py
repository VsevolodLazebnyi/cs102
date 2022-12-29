from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param coord:
    :return:
    """
    # 2. выбрать направление: наверх или направо.
    var = [(-1, 0), (0, 1)]
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    way = choice(var)
    if coord[0] != 1 or coord[1] != len(grid[0]) - 2:
        if coord[0] + way[0] < 1 or coord[1] + way[1] > len(grid[0]) - 2:
            # способ заменить выбор на другой
            way = var[var[0] == way]
        # 3. перейти в следующую клетку, сносим между клетками стену
        grid[coord[0] + way[0]][coord[1] + way[1]] = " "
    return grid


def bin_tree_maze(rows: int = 15, cols: int = 15, random_exit: bool = True) -> List[List[Union[str, int]]]:
    """
    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """
    # уже было
    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))
    # 1. выбрать любую клетку 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки
    for coord in empty_cells:
        grid = remove_wall(grid, coord)
    # было в самом коде
    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """
    :param grid:
    :return:
    """
    # ищет координаты иксов
    coord = list()
    for i, r in enumerate(grid):
        for j, c in enumerate(r):
            if c == "X":
                coord.append((i, j))
    return coord


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param k:
    :return:
    """
    # ходим, пока не набрядем на вход
    xrange = len(grid)
    yrange = len(grid[0])
    for x in range(xrange):
        for y in range(yrange):
            if grid[x][y] == k:
                if x > 0 and grid[x - 1][y] == 0:
                    grid[x - 1][y] = k + 1
                if x < xrange - 1 and grid[x + 1][y] == 0:
                    grid[x + 1][y] = k + 1
                if y > 0 and grid[x][y - 1] == 0:
                    grid[x][y - 1] = k + 1
                if y < yrange - 1 and grid[x][y + 1] == 0:
                    grid[x][y + 1] = k + 1
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """
    :param grid:
    :param exit_coord:
    :return:
    """
    path = []
    pos = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    while grid[exit_coord[0]][exit_coord[1]] != 1:
        k = int(grid[exit_coord[0]][exit_coord[1]])
        for i in pos:
            if 0 <= exit_coord[0] + i[0] < len(grid) and 0 <= exit_coord[1] + i[1] < len(grid[0]):
                if type(grid[exit_coord[0] + i[0]][exit_coord[1] + i[1]]) is int and \
                        grid[exit_coord[0] + i[0]][exit_coord[1] + i[1]] == k - 1:
                    path.append(exit_coord)
                    exit_coord = (exit_coord[0] + i[0], exit_coord[1] + i[1])
                    break
    path.append(exit_coord)
    return path


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """
    :param grid:
    :param coord:
    :return:
    """

    xrange = len(grid)
    yrange = len(grid[0])
    # смотрим углы
    if coord in [(0, 0), (xrange - 1, 0), (0, yrange - 1), (xrange - 1, yrange - 1)]:
        return True
    # смотрим пусто ли вокруг входа
    return (
            coord[0] == 0
            and grid[coord[0] + 1][coord[1]] != " "
            or coord[1] == 0
            and grid[coord[0]][coord[1] + 1] != " "
            or coord[0] == xrange - 1
            and grid[coord[0] - 1][coord[1]] != " "
            or coord[1] == xrange - 1
            and grid[coord[0]][coord[1] - 1] != " "
    )
    # а чё ещё остаётся?)))


def solve_maze(
    grid: List[List[Union[str, int]]],
) -> Tuple[List[List[Union[str, int]]], Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]]:
    """
    :param grid:
    :return:
    """

    exs = get_exits(grid)
    # 1. проверяем, что выходов больше одного (помним, мы можем задавать их
    # случайным образом). Если это не правда - путь найден, это координаты
    # входа (она же координата выхода). Возвращаем лабиринт и координаты
    if len(exs) < 2:
        return grid, exs[0]

    # 2. если все же выходов два, проверяем, что мы не в тупике. Если в тупике,
    # возвращаем None, пути нет
    if encircled_exit(grid, exs[0]) or encircled_exit(grid, exs[1]):
        return grid, None

    # 3. если мы не в тупике, реализуем нашу версию алгоритма Дейкстры
    # возвращаем лабиринт и путь
    grid = deepcopy(grid)
    ent, ext = exs[0], exs[1]
    grid[ent[0]][ent[1]], grid[ext[0]][ext[1]] = 1, 0
    for x in range(len(grid) - 1):
        for y in range(len(grid[0]) - 1):
            if grid[x][y] == " ":
                grid[x][y] = 0
    step = 1
    while grid[ext[0]][ext[1]] == 0:
        make_step(grid, step)
        step += 1
    path = shortest_path(grid, ext)
    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]], path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]
) -> List[List[Union[str, int]]]:
    """
    :param grid:
    :param path:
    :return:
    """

    if path:
        for x, r in enumerate(grid):
            for y, c in enumerate(r):
                if (x, y) in path:
                    grid[x][y] = "X"
    return grid


if __name__ == "__main__":
    GRID = bin_tree_maze(15, 15)
    _, PATH = solve_maze(GRID)
    MAZE = add_path_to_grid(GRID, PATH)
