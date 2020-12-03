import typing


class Grid:
    def __init__(self, grid: typing.List[str]):
        assert len(grid) > 0
        assert all(len(row) == len(grid[0]) for row in grid)
        self._grid = grid
        self.y_max = len(grid)
        self._x_max = len(grid[0])

    def is_tree(self, x: int, y: int) -> bool:
        return '#' == self._grid[y][x % self._x_max]


def solve(grid: Grid, slopes: typing.List[typing.Tuple[int, int]]) -> int:
    tree_count_product = 1
    for delta_x, delta_y in slopes:
        x, y, tree_count = 0, 0, 0
        while y < grid.y_max:
            tree_count += grid.is_tree(x, y)
            x += delta_x
            y += delta_y
        tree_count_product *= tree_count
    return tree_count_product


if __name__ == '__main__':
    with open('dec03.input', 'r') as f:
        my_grid = Grid(f.read().splitlines())
    print(solve(my_grid, [(3, 1)]))
    print(solve(my_grid, [(1, 1), (3, 1), (5, 1), (7, 1), (1, 2)]))
