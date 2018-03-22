from abc import abstractmethod, ABC
from decimal import Decimal
from re import match
from typing import List


class Operation(ABC):
    def __init__(self, number: Decimal, symbol):
        if isinstance(number, str):
            number = Decimal(number)
        self.number = number
        self.symbol = symbol

    def __eq__(self, other):
        return type(self) == type(other) and self.number == other.number

    def __repr__(self):
        t = type(self)
        m, n = t.__module__, t.__name__
        return '<{}.{} object; {} >'.format(m, n, str(self))

    def __str__(self):
        return '{}{}'.format(self.symbol, self.number)

    @abstractmethod
    def __call__(self, arg: Decimal) -> Decimal:
        raise NotImplementedError()


class NumberOperation(Operation):
    def __init__(self, number: Decimal):
        super().__init__(number, '')

    def __call__(self, arg: Decimal) -> Decimal:
        return Decimal(str(arg) + str(self.number))


class AddOperation(Operation):
    def __init__(self, number: Decimal):
        super().__init__(number, '+')

    def __call__(self, arg: Decimal) -> Decimal:
        return arg + self.number


class DiffOperation(Operation):
    def __init__(self, number: Decimal):
        super().__init__(number, '-')

    def __call__(self, arg: Decimal) -> Decimal:
        return arg - self.number


class MultiplyOperation(Operation):

    def __init__(self, number: Decimal):
        super().__init__(number, '*')

    def __call__(self, arg: Decimal) -> Decimal:
        return arg * self.number


class DivideOperation(Operation):

    def __init__(self, number: Decimal):
        super().__init__(number, '/')

    def __call__(self, arg: Decimal) -> Decimal:
        return arg / self.number


class DeleteOperation(Operation):
    def __init__(self, number=None):
        super().__init__(number, '<<')

    def __call__(self, arg: Decimal) -> Decimal:
        return Decimal(str(arg)[:-1] or '0')

    def __str__(self):
        return '{}'.format(self.symbol)


class ConvertNumOperation(Operation):
    def __init__(self, old: Decimal, new: Decimal):
        # noinspection PyTypeChecker
        super().__init__(None, '=>')
        if isinstance(old, str):
            old = Decimal(old)
        self.old = old

        if isinstance(new, str):
            new = Decimal(new)
        self.new = new

    def __call__(self, arg: Decimal) -> Decimal:
        return Decimal(str(arg).replace(str(self.old), str(self.new)))

    def __eq__(self, other):
        return type(self) == type(other) and self.old == other.old and self.new == other.new

    def __str__(self):
        return '{}{}{}'.format(self.old, self.symbol, self.new)


op_names = {None: NumberOperation,
            '+': AddOperation,
            '-': DiffOperation,
            '*': MultiplyOperation,
            'x': MultiplyOperation,
            '/': DivideOperation,
            '<<': DeleteOperation,
            '=>': ConvertNumOperation}


def parse_operation(op_str: str) -> Operation:
    parts = match(r'((\d+)?([+\-*x/%]|<<|=>))?(\d+)?', op_str)
    if parts:
        _, pre_num, sign, post_num, = parts.groups()
        if sign == '=>':
            rv = op_names[sign](pre_num, post_num)
        else:
            rv = op_names[sign](post_num)
        return rv


def parse_operations(ops_str: str) -> List[Operation]:
    return [parse_operation(op_str) for op_str in ops_str.split(' ')]


class MGS():
    def __init__(self, start: Decimal, goal: Decimal, step_count: int, operations: List[Operation]):
        self.start = start
        self.goal = goal
        self.step_count = step_count
        self.operations = operations

    def solve(self) -> List[Operation]:
        if self.step_count == 0:
            return []

        for op in self.operations:
            candidate_start = op(self.start)
            if candidate_start == self.goal:
                return [op]
            else:
                solution = MGS(candidate_start, self.goal, self.step_count - 1, self.operations).solve()
                if len(solution):
                    solution.insert(0, op)
                    return solution

        return []

    def __repr__(self):
        t = type(self)
        m, n = t.__module__, t.__name__
        return '<{}.{} object; start={}, goal={}, steps={}>'.format(m, n, self.start, self.goal, self.step_count)


def render_ops(operations: List[Operation]):
    return ' '.join(str(op) for op in operations)


if __name__ == '__main__':
    levels_from_25 = [
        MGS(start=Decimal(40),
            goal=Decimal(2020),
            step_count=4,
            operations=parse_operations('0 +4 /2')),
        MGS(start=Decimal(0),
            goal=Decimal(11),
            step_count=4,
            operations=parse_operations('12 <<')),
        MGS(start=Decimal(0),
            goal=Decimal(102),
            step_count=4,
            operations=parse_operations('10 +1 <<')),
        ##############introduced ConvertNumberOperation
        MGS(start=Decimal(0),
            goal=Decimal(222),
            step_count=4,
            operations=parse_operations('1 1=>2')),

        MGS(start=Decimal(0),
            goal=Decimal(93),
            step_count=4,
            operations=parse_operations('+6 x7 6=>9')),

        MGS(start=Decimal(0),
            goal=Decimal(2321),
            step_count=6,
            operations=parse_operations('1 2 1=>2 2=>3')),
        MGS(start=Decimal(0),
            goal=Decimal(24),
            step_count=6,
            operations=parse_operations('+9 x2 8=>4')),
        MGS(start=Decimal(11),
            goal=Decimal(29),
            step_count=5,
            operations=parse_operations('/2 +3 1=>2 2=>9')),
    ]

    for level in levels_from_25:
        solution = level.solve()
        print('|{:5}|{:6}|{:2}|{:20}|{:22}|'.format(level.start,
                                                    level.goal,
                                                    level.step_count,
                                                    render_ops(level.operations),
                                                    render_ops(solution)))
