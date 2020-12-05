import typing


class BoardingPass:
    def __init__(self, boarding_pass: str):
        self.row = self._get_index(
            directions=boarding_pass[:7],
            lower=0,
            upper=127,
            higher_character='B'
        )
        self.column = self._get_index(
            directions=boarding_pass[7:],
            lower=0,
            upper=7,
            higher_character='R'
        )
        self.seat_id = self.row * 8 + self.column

    @staticmethod
    def _get_index(directions: str, lower: int, upper: int, higher_character: str):
        for direction in directions:
            mid = (lower + upper) // 2
            if direction == higher_character:
                lower = mid + 1
            else:
                upper = mid
        assert upper == lower
        return lower


def solve(boarding_passes: typing.List[BoardingPass]):
    boarding_passes.sort(key=lambda bp: bp.seat_id)
    yield boarding_passes[-1].seat_id

    expected_seat_ids = range(boarding_passes[0].seat_id, boarding_passes[-1].seat_id)
    for expected_id, boarding_pass in zip(expected_seat_ids, boarding_passes):
        if expected_id != boarding_pass.seat_id:
            yield expected_id
            return


if __name__ == '__main__':
    with open('dec05.input', 'r') as f:
        passengers = list(map(BoardingPass, f.read().splitlines()))
    solution_generator = solve(passengers)
    print('Part 1', next(solution_generator))
    print('Part 2', next(solution_generator))
