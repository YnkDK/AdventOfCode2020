import collections
import operator


class ChildMath:
    _OPERATOR = {
        '+': operator.add,
        '*': operator.mul
    }
    _LEFT_PARENTHESIS = '('
    _RIGHT_PARENTHESIS = ')'

    def __init__(self):
        self._output = collections.deque()
        self._operators = collections.deque()

    def solve(self, expression: str):
        for token in expression:
            if token == " ":
                continue
            try:
                self._output.append(int(token))
            except ValueError:
                self._handle_non_int(token)

        while len(self._operators) > 0:
            self._execute()

        assert len(self._output) == 1, 'Mismatch between operators and outputs'
        return self._output.pop()

    def _handle_non_int(self, token: str):
        try:
            op = ChildMath._OPERATOR[token]
        except KeyError:
            if token == ChildMath._RIGHT_PARENTHESIS:
                while len(self._operators) > 0 and self._operators[-1] != ChildMath._LEFT_PARENTHESIS:
                    self._execute()
                assert self._operators[-1] == ChildMath._LEFT_PARENTHESIS
                self._operators.pop()
            else:
                assert token == ChildMath._LEFT_PARENTHESIS, f'Expected (, but got "{token}"'
                self._operators.append(token)
        else:
            while len(self._operators) > 0 and self._operators[-1] != ChildMath._LEFT_PARENTHESIS:
                self._execute()
            self._operators.append(op)

    def _execute(self):
        op = self._operators.pop()
        b = self._output.pop()
        a = self._output.pop()
        res = op(a, b)
        self._output.append(res)


def solve(expressions: list):
    child_math = ChildMath()
    total = sum(map(child_math.solve, expressions))
    yield total


if __name__ == '__main__':
    with open('dec18.input', 'r') as f:
        dec18 = f.read().split('\n')
    solutions = solve(dec18)
    print('Part 1:', next(solutions))
