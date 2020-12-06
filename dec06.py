from typing import List


class GroupAnswers:
    def __init__(self, raw_group_answers: str):
        _group_answers = list(map(set, raw_group_answers.split('\n')))
        self.anyone_answered = set.union(*_group_answers)
        self.all_answered = set.intersection(*_group_answers)


def parse_input(raw: str):
    return list(map(GroupAnswers, raw.split('\n\n')))


def solve(answers: List[GroupAnswers]):
    yield sum(len(answer.anyone_answered) for answer in answers)
    yield sum(len(answer.all_answered) for answer in answers)


if __name__ == '__main__':
    with open('dec06.input', 'r') as f:
        group_answers = parse_input(f.read())
    solution_generator = solve(group_answers)
    print('Part 1', next(solution_generator))
    print('Part 2', next(solution_generator))
