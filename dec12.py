from enum import Enum


class Actions(Enum):
    EAST = 'E'
    SOUTH = 'S'
    WEST = 'W'
    NORTH = 'N'
    RIGHT = 'R'
    LEFT = 'L'
    FORWARD = 'F'


class Ferry:
    _ROTATIONS = {
        0: Actions.EAST,
        90: Actions.SOUTH,
        180: Actions.WEST,
        270: Actions.NORTH
    }

    def __init__(self):
        self._rotation = 0
        self._direction = Ferry._ROTATIONS[self._rotation]
        self._distances = {
            Actions.EAST: 0,
            Actions.SOUTH: 0,
            Actions.WEST: 0,
            Actions.NORTH: 0
        }

    def reset(self):
        self._rotation = 0
        self._direction = Ferry._ROTATIONS[self._rotation]
        self._distances = {
            Actions.EAST: 0,
            Actions.SOUTH: 0,
            Actions.WEST: 0,
            Actions.NORTH: 0
        }

    def move(self, instruction: str):
        action = Actions(instruction[0])
        argument = int(instruction[1:])
        if action in (Actions.RIGHT, Actions.LEFT):
            if action == Actions.LEFT:
                argument *= -1
            self._rotation = (self._rotation + argument) % 360
            self._direction = Ferry._ROTATIONS[self._rotation]
            return
        if action == Actions.FORWARD:
            action = self._direction

        self._distances[action] += argument

    @property
    def manhattan_distance_moved(self):
        west = abs(self._distances[Actions.EAST] - self._distances[Actions.WEST])
        north = abs(self._distances[Actions.NORTH] - self._distances[Actions.SOUTH])
        return west + north


def solve(instructions):
    ferry = Ferry()
    for instruction in instructions:
        ferry.move(instruction)
    yield ferry.manhattan_distance_moved


if __name__ == '__main__':
    with open('dec12.input', 'r') as f:
        dec12 = f.readlines()
    solution_generator = solve(dec12)

    print('Part 1:', next(solution_generator))
