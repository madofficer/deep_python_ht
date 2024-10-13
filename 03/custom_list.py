class CustomList(list):
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        elif not isinstance(iterable, (list, tuple, set, frozenset, dict)):
            raise TypeError(
                f"Expected types are: 'list', 'tuple', 'set', "
                f"'frozenset', 'dict', got {type(iterable).__name__} instead"
            )
        if not all(isinstance(i, (int, float)) for i in iterable):
            raise TypeError(
                "All elements of the iterable object must be 'int' or 'float'"
            )
        super().__init__(iterable)

    def __str__(self):
        return f"{list(self)} = {sum(self)}"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return CustomList([i + other for i in self])
        elif isinstance(other, (list, tuple)):
            max_len = max(len(self), len(other))
            res = [0] * max_len
            for i in range(max_len):
                if i >= len(self):
                    res[i] = other[i]
                elif i >= len(other):
                    res[i] = self[i]
                else:
                    res[i] = self[i] + other[i]
            return CustomList(res)
        else:
            raise TypeError(
                f"Unsupported operand type(s) for +: 'CustomList' "
                f"and '{type(other).__name__}'"
            )

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return self + (-other)
        elif isinstance(other, (list, tuple)):
            return self + [-i for i in other]
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: 'CustomList' "
                f"and '{type(other).__name__}"
            )

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return CustomList([other - i for i in self])
        elif isinstance(other, list):
            return CustomList([-i for i in self]) + other
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: '{type(other).__name__}' "
                f"and 'CustomList'"
            )

    def __eq__(self, other):
        return sum(self) == sum(other)

    def __ne__(self, other):
        return sum(self) != sum(other)

    def __ge__(self, other):
        return sum(self) >= sum(other)

    def __le__(self, other):
        return sum(self) <= sum(other)

    def __gt__(self, other):
        return sum(self) > sum(other)

    def __lt__(self, other):
        return sum(self) < sum(other)


if __name__ == "__main__":
    a = CustomList()
    a.append(100)
    a.append(1000)
    print(a + 5)
    print(5 + a)
    print(len(a))
    print(a + [67])
    print(a + a)
    print(a)
    print(a - 123)
    print(a - [123])
    print(a - [123, 456, 999])
    print(a)
    print([1000, 1000, 1000] - a)
    b = CustomList([99, 99, 4561])
    print(a + b)
    print(a - b)
    print(a > b)
    print(a + (-1))
    print(-1 - a)
    b = CustomList((1, 2, 3))
    c = CustomList({1, 2, 5})
    print(c)
    print(b + (1, 2, 3))
    # d = CustomList('45345')
    # print(d)
