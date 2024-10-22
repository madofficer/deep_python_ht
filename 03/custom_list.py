from collections.abc import Iterable


class CustomList(list):
    def __init__(self, iterable=None):
        if iterable is None:
            iterable = []
        elif not isinstance(iterable, Iterable):
            raise TypeError(
                f"Expected an iterable object, "
                f"got {type(iterable).__name__} instead"
            )
        iterable = list(iterable)
        if not all(isinstance(i, (int, float)) for i in iterable):
            raise TypeError(
                "All elements of the iterable object must be 'int' or 'float'"
            )
        super().__init__(iterable)

    def __str__(self):
        return f"{list(self)} = {sum(self)}"

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return CustomList(
                [
                    round(i + other, 4)
                    if isinstance(i + other, float)
                    else i + other
                    for i in self
                ]
            )
        elif isinstance(other, (list, tuple)):
            max_len = max(len(self), len(other))
            res = [0] * max_len
            for i in range(max_len):
                if i >= len(self):
                    res[i] = other[i]
                elif i >= len(other):
                    res[i] = self[i]
                else:
                    res[i] = (
                        round(self[i] + other[i], 4)
                        if isinstance(self[i] + other[i], float)
                        else self[i] + other[i]
                    )
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
            return CustomList(
                [
                    (
                        round(i - other, 4)
                        if isinstance(i - other, float)
                        else i - other
                    )
                    for i in self
                ]
            )
        elif isinstance(other, (list, tuple)):
            return self + [
                round(-i, 4)
                if isinstance(i, float)
                else -i for i in other
                           ]
        else:
            raise TypeError(
                f"Unsupported operand type(s) for -: 'CustomList' "
                f"and '{type(other).__name__}"
            )

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return CustomList(
                [
                    round(other - i, 4)
                    if isinstance(other - i, float)
                    else other - i
                    for i in self
                ]
            )
        elif isinstance(other, (list, tuple)):
            return (
                CustomList([round(-i, 4)
                            if isinstance(i, float)
                            else -i for i in self]) + other
            )
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


# if __name__ == "__main__":
    # a = CustomList()
    # a.append(100)
    # a.append(1000)
    # print(a + 5)
    # print(5 + a)
    # print(len(a))
    # print(a + [67])
    # print(a + a)
    # print(a)
    # print(a - 123)
    # print(a - [123])
    # print(a - [123, 456, 999])
    # print(a)
    # print([1000, 1000, 1000] - a)
    # b = CustomList([99, 99, 4561])
    # print(a + b)
    # print(a - b)
    # print(a > b)
    # print(a + (-1))
    # print(-1 - a)
    # b = CustomList((1, 2, 3))
    # c = CustomList({1, 2, 5})
    # print(c)
    # print(b + (1, 2, 3))
    # d = CustomList('45345')
    # print(d)
    # n = CustomList(range(1, 11, 2))
    # print(n.get_items())
    # res = (n + 10).get_items()
    # print(type(res))
    # x = CustomList([1, 2, 3])
    # y = CustomList([6])
    # a = [5, 1, 3, 7]
    # a1 = a.copy()
    # a_custom = CustomList(a)
    # b = [1, 2, 7]
    # b1 = b.copy()
    # b_custom = CustomList(b)
    # res = a_custom - 0
    # ans = CustomList([i - 0 for i in a])
    # print(res)
    # print(ans)
    # print(type(list(ans)))
    # iter_a = iter(a)
    # print(CustomList(iter_a))
    # print(CustomList(iter(a)) == CustomList(a1))
    # print((list(iter(a))))
    # print((list(iter(a))))
