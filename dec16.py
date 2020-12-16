import re


class Field:
    _PATTERN = re.compile(r'^([a-z ]+): (\d+)-(\d+) or (\d+)-(\d+)$')

    def __init__(self, field_notes: str):
        try:
            groups = Field._PATTERN.match(field_notes).groups()
        except AttributeError:
            import sys
            print(f'Could not parse {field_notes}', file=sys.stderr)
            raise
        self.name = groups[0]
        l1 = int(groups[1])
        h1 = int(groups[2])
        l2 = int(groups[3])
        h2 = int(groups[4])
        self.validator = lambda x: l1 <= x <= h1 or l2 <= x <= h2

    @property
    def is_departure_information(self):
        return self.name.startswith('departure')

    def __repr__(self):
        return self.name


class TicketTranslator:
    def __init__(self, notes: str):
        fields, my_ticket, nearby_tickets = notes.split('\n\n')

        self._fields = [Field(field) for field in fields.split('\n')]
        self._my_ticket = TicketTranslator._parse_ticket(my_ticket.split('\n')[1])
        self._nearby_tickets = [TicketTranslator._parse_ticket(ticket) for ticket in nearby_tickets.split('\n')[1:]]

    def remove_invalid_nearby_tickets(self):
        ticket_scanning_error_rate = 0
        i = 0
        n = len(self._nearby_tickets)
        while i < n:
            ticket = self._nearby_tickets[i]
            for unknown_field in ticket:
                if not any(field.validator(unknown_field) for field in self._fields):
                    ticket_scanning_error_rate += unknown_field
                    del self._nearby_tickets[i]
                    n -= 1
                    break
            else:
                i += 1
        return ticket_scanning_error_rate

    def translate(self):
        candidates = []
        candidates_determined = []
        for i in range(len(self._fields)):
            candidates_for_field = []
            for field in self._fields:
                if all(field.validator(ticket[i]) for ticket in self._nearby_tickets):
                    candidates_for_field.append(field)
            candidates.append(candidates_for_field)
            if len(candidates_for_field) == 1:
                candidates_determined.append(candidates_for_field[0])

        while len(candidates_determined) > 0:
            field = candidates_determined.pop()
            for candidate_list in candidates:
                if len(candidate_list) > 1:
                    # raises a ValueError if there is no such item, but not encountered
                    candidate_list.remove(field)
                    if len(candidate_list) == 1:
                        candidates_determined.append(candidate_list[0])

        assert all(len(candidate) == 1 for candidate in candidates), f'Sanity check failed: {candidates}'
        self._fields = [candidate[0] for candidate in candidates]

    @property
    def my_ticket(self):
        return dict((field, value) for field, value in zip(self._fields, self._my_ticket))

    @staticmethod
    def _parse_ticket(line: str):
        return tuple(map(int, line.split(',')))


def solve(ticket_translator: TicketTranslator):
    yield ticket_translator.remove_invalid_nearby_tickets()

    ticket_translator.translate()
    my_ticket = ticket_translator.my_ticket
    product = 1
    for field, value in my_ticket.items():
        if field.is_departure_information:
            product *= value
    yield product


if __name__ == '__main__':
    with open('dec16.input', 'r') as f:
        dec16 = f.read()

    tt = TicketTranslator(dec16)
    solutions = solve(tt)

    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
