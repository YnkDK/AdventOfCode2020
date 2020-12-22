import collections
import operator

Operator = collections.namedtuple('Operator', ('operator', 'precedence_level'))


class ChildMath:
    _OPERATOR = {
        '+': operator.add,
        '*': operator.mul
    }
    _LEFT_PARENTHESIS = '('
    _RIGHT_PARENTHESIS = ')'

    def __init__(self):
        self._output = collections.deque()  # type: collections.deque[int]
        self._operators = collections.deque()  # type: collections.deque[Operator]
        self._precedence_levels = {
            '*': 1,
            '+': 1,
            '(': 0
        }
        self._left_parenthesis_operator = Operator(
            ChildMath._LEFT_PARENTHESIS,
            self._precedence_levels[ChildMath._LEFT_PARENTHESIS]
        )

    def solve(self, expression: str):
        """Simple implementation of the Shunting-yard algorithm with the rules given by Advent of Code.

        The state is clean after each execution, so this method can be called multiple times.

        See `Wikipedia: Shunting-yard algorithm <https://en.wikipedia.org/wiki/Shunting-yard_algorithm>`_

        :param expression: The expression to be evaluated.
        :return: The result after evaluation.
        """
        for token in expression:
            if token == " ":
                continue

            try:
                # if the token is a number, then:
                #     push it to the output queue.
                self._output.append(int(token))
            except ValueError:
                self._handle_non_int(token)

        # while there are still operator tokens on the stack:
        while len(self._operators) > 0:
            # pop the operator from the operator stack onto the output queue.
            self._execute()

        assert len(self._output) == 1, 'Mismatch between operators and outputs'
        return self._output.pop()

    def switch_to_advanced_math(self):
        """Sets the addition (+) operator to have higher precedence level than multiplication (*) operator.
        """
        self._precedence_levels = {
            '*': 2,
            '+': 1,
            '(': 0
        }
        self._left_parenthesis_operator = Operator(
            ChildMath._LEFT_PARENTHESIS,
            self._precedence_levels[ChildMath._LEFT_PARENTHESIS]
        )

    def _handle_non_int(self, token: str):
        try:
            op = ChildMath._OPERATOR[token]
        except KeyError:
            if token == ChildMath._RIGHT_PARENTHESIS:
                # while the operator at the top of the operator stack is not a left parenthesis:
                while self._operators[-1].operator != ChildMath._LEFT_PARENTHESIS:
                    # pop the operator from the operator stack onto the output queue.
                    self._execute()
                # pop the operator from the operator stack and discard it
                left_parenthesis = self._operators.pop()
                assert left_parenthesis.operator == ChildMath._LEFT_PARENTHESIS
            else:
                assert token == ChildMath._LEFT_PARENTHESIS, f'Expected (, but got "{token}"'
                # else if the token is a left parenthesis (i.e. "("), then:
                #     push it onto the operator stack.
                self._operators.append(self._left_parenthesis_operator)
        else:
            op = Operator(op, self._precedence_levels[token])
            # while ((there is an operator at the top of the operator stack)
            #       and ((the operator at the top of the operator stack has greater precedence)
            #           or (the operator at the top of the operator stack has equal precedence))
            #       and (the operator at the top of the operator stack is not a left parenthesis)):
            while len(self._operators) > 0 \
                    and self._operators[-1].precedence_level <= op.precedence_level \
                    and self._operators[-1].operator != ChildMath._LEFT_PARENTHESIS:
                # pop operators from the operator stack onto the output queue.
                self._execute()
            # push it onto the operator stack.
            self._operators.append(op)

    def _execute(self):
        op = self._operators.pop()
        b = self._output.pop()
        a = self._output.pop()
        res = op.operator(a, b)
        self._output.append(res)


def solve(expressions: list):
    child_math = ChildMath()
    total = sum(map(child_math.solve, expressions))
    yield total

    child_math.switch_to_advanced_math()
    total = sum(map(child_math.solve, expressions))
    yield total


if __name__ == '__main__':
    with open('dec18.input', 'r') as f:
        dec18 = f.read().split('\n')
    solutions = solve(dec18)
    print('Part 1:', next(solutions))
    print('Part 2:', next(solutions))
