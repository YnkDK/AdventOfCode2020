from collections import namedtuple

Bus = namedtuple('Bus', ('identifier', 'wait_time'))


class BusNotes:
    def __init__(self, departure_identifiers: str):
        self._departure_identifiers = []
        self._offsets = []
        self._max_time = 0
        for offset, identifier in enumerate(departure_identifiers.split(',')):
            try:
                i = int(identifier)
                if i > self._max_time:
                    self._max_time = i
                self._departure_identifiers.append(i)
                self._offsets.append(offset)
            except ValueError:
                continue

    def first_bus(self, earliest_departure_time: int) -> Bus:
        first_bus = Bus(self._max_time, self._max_time)
        for identifier in self._departure_identifiers:
            wait_time = identifier - (earliest_departure_time % identifier)
            if wait_time == identifier:
                return Bus(identifier, 0)
            if wait_time < first_bus.wait_time:
                first_bus = Bus(identifier, wait_time)
        return first_bus

    def shuttle_company_contest(self):
        print(self._departure_identifiers)
        print(self._offsets)
        t = 1
        while True:
            j = 0
            while j < len(self._offsets):
                if t % self._departure_identifiers[j] != self._offsets[j]:
                    break
                j += 1
            if j == len(self._offsets):
                return t
            t += 1


def solve(bus_notes: BusNotes, earliest_departure_time: int):
    first_bus = bus_notes.first_bus(earliest_departure_time)
    yield first_bus.wait_time * first_bus.identifier
    yield bus_notes.shuttle_company_contest()


if __name__ == '__main__':
    with open('dec13.input', 'r') as f:
        edt, n = f.readlines()
    bn = BusNotes(n)
    solutions = solve(bn, int(edt))

    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
