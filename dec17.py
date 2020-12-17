import itertools


class ConwayCubes:
    def __init__(self, initial_state: str, dimensions: int = 3):
        active_state = '#'
        self._state = set()
        for x, row in enumerate(initial_state.split('\n')):
            for y, cube in enumerate(row):
                if cube == active_state:
                    origin = [0] * dimensions
                    origin[0] = x
                    origin[1] = y
                    self._state.add(tuple(origin))

    def run_cycle(self):
        new_state = set()
        candidates = self._get_candidates()
        for candidate in candidates:
            if self.is_active(candidate):
                should_add_candidate = self._process_active_cube(candidate)
            else:
                should_add_candidate = self._process_inactive_cube(candidate)

            if should_add_candidate:
                new_state.add(candidate)
        self._state = new_state

    def is_active(self, cube):
        return cube in self._state

    @property
    def active_count(self):
        return len(self._state)

    def _get_candidates(self):
        candidates = set()
        for cube in self._state:
            candidates.add(cube)
            candidates = candidates.union(set(self._neighbour_generator(cube)))
        return candidates

    def _process_active_cube(self, cube):
        neighbour_active_count = 0
        for neighbour in self._neighbour_generator(cube):
            neighbour_active_count += self.is_active(neighbour)
            if neighbour_active_count > 3:
                return False
        return neighbour_active_count in (2, 3)

    def _process_inactive_cube(self, cube):
        neighbour_active_count = 0
        for neighbour in self._neighbour_generator(cube):
            neighbour_active_count += self.is_active(neighbour)
            if neighbour_active_count > 3:
                return False
        return neighbour_active_count == 3

    @staticmethod
    def _neighbour_generator(cube):
        dimensions = len(cube)
        all_deltas = list(itertools.product([-1, 0, 1], repeat=dimensions))
        all_deltas.remove((0,) * dimensions)

        for deltas in all_deltas:
            neighbour = []
            for current, delta in zip(cube, deltas):
                neighbour.append(current + delta)
            yield tuple(neighbour)


def solve(initial_state: str):
    conway_cubes = ConwayCubes(initial_state)
    for _ in range(6):
        conway_cubes.run_cycle()
    yield conway_cubes.active_count

    conway_cubes = ConwayCubes(initial_state, 4)
    for _ in range(6):
        conway_cubes.run_cycle()
    yield conway_cubes.active_count


if __name__ == '__main__':
    with open('dec17.input', 'r') as f:
        dec17 = f.read()

    solutions = solve(dec17)

    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
