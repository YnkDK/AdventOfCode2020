OCCUPIED_SEAT = '#'
EMPTY_SEAT = 'L'
FLOOR = '.'
ADJACENT_MODE = 'adj'
LINE_OF_SIGHT_MODE = 'los'


class SeatingSystem:

    def __init__(self, grid: str, max_tolerated_occupied: int = 4, mode: str = ADJACENT_MODE):
        self._grid = grid.split('\n')
        self._max_tolerated_occupied = max_tolerated_occupied
        if mode == ADJACENT_MODE:
            self._seat_generator = self._adjacent_seat_generator
        elif mode == LINE_OF_SIGHT_MODE:
            self._seat_generator = self._line_of_sight_seat_generator
        else:
            raise NotImplemented(f'Unsupported mode: {mode}')

    def run_simulation(self):
        """Runs the simulation until the chaos stabilizes and further applications of these rules cause no seats to
        change state!
        """
        generator = self.rounds()
        while next(generator):
            pass

    def rounds(self):
        """A generator that simulate a single round.

        Applies the configured rules to every seat simultaneously for each round.

        :return: If the grid changed or not
        """
        did_change = True
        while did_change:
            new_grid = []
            did_change = False
            for i in range(len(self._grid)):
                new_row = []
                for j in range(len(self._grid[i])):
                    current_state = self._grid[i][j]
                    new_state = self._apply_rule(i, j)
                    did_change |= current_state != new_state
                    new_row.append(new_state)
                new_grid.append(new_row)

            self._grid = new_grid
            yield did_change

    @property
    def number_of_seats_occupied(self):
        """Counts the number of seats occupied in the grid in its current state.

        :return: Number of occupied seats.
        """
        return sum(s.count(OCCUPIED_SEAT) for s in self._grid)

    def _apply_rule(self, i, j):
        """Find the new state for the seat (or floor) at a given point.

        Rules:
        1) Floor (.) never changes; seats don't move, and nobody sits on the floor.
        2) If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
        3) If a seat is occupied (#) and max_tolerated_occupied or more seats adjacent to it are also occupied,
           the seat becomes empty.
        4) Otherwise, the seat's state does not change.

        Adjacent: Depends on the mode.

        :param i: The row index of the seat to apply the rule to.
        :param j: The column index of the seat to apply the rule to.
        :return: The new state of the seat (or floor) at a given point.
        """
        current_state = self._grid[i][j]
        if current_state == FLOOR:
            # Floor (.) never changes; seats don't move, and nobody sits on the floor.
            return current_state
        if current_state == EMPTY_SEAT:
            # If a seat is empty (L) and there are no occupied seats adjacent to it, the seat becomes occupied.
            if any(seat == OCCUPIED_SEAT for seat in self._seat_generator(i, j)):
                return current_state
            # Otherwise, the seat's state does not change.
            return OCCUPIED_SEAT
        if current_state == OCCUPIED_SEAT:
            # If a seat is occupied (#) and four or more seats adjacent to it are also occupied, the seat becomes empty.
            if sum(seat == OCCUPIED_SEAT for seat in self._seat_generator(i, j)) >= self._max_tolerated_occupied:
                return EMPTY_SEAT
            # Otherwise, the seat's state does not change.
            return current_state
        raise NotImplemented(f'Not implemented rule for "{current_state}"')

    def _adjacent_seat_generator(self, i, j) -> str:
        """Considers all the eight immediately adjacent seats.

        :param i: The row index of the seat start from.
        :param j: The column index of the seat to start from.
        :return: All seat states (occupied, empty or floor) in line of sight of the starting point.
        """
        for k in (i - 1, i, i + 1):
            if k < 0 or k >= len(self._grid):
                continue
            for m in (j - 1, j, j + 1):
                if m < 0 or m >= len(self._grid[k]) or k == i and m == j:
                    continue
                yield self._grid[k][m]

    def _line_of_sight_seat_generator(self, i: int, j: int) -> str:
        """Considers not just the eight immediately adjacent seats, but considers the first seat in each of those eight
        directions.

        :param i: The row index of the seat start from.
        :param j: The column index of the seat to start from.
        :return: All seat states (occupied or empty) in line of sight of the starting point.
        """
        for kd, md in ((-1, 0), (1, 0), (0, -1), (0, 1), (-1, 1), (-1, -1), (1, -1), (1, 1)):
            k = i + kd
            m = j + md
            while 0 <= k < len(self._grid) and 0 <= m < len(self._grid[k]):
                state = self._grid[k][m]
                if state == FLOOR:
                    k += kd
                    m += md
                    continue
                yield state
                break

    def __repr__(self):
        return '\n'.join([''.join(row) for row in self._grid])


def solve(seating_system: str):
    system = SeatingSystem(seating_system)
    system.run_simulation()
    yield system.number_of_seats_occupied

    system = SeatingSystem(seating_system, 5, LINE_OF_SIGHT_MODE)
    system.run_simulation()
    yield system.number_of_seats_occupied


if __name__ == '__main__':
    with open('dec11.input', 'r') as f:
        dec11 = f.read()
    solution_generator = solve(dec11)

    print('Part 1:', next(solution_generator))
    print('Part 2:', next(solution_generator))
