class CustomList(list):

    def __str__(self):
        return f'{list(self)} = {sum(self)}'

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return CustomList([i + other for i in self])
        elif isinstance(other, list):
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
            raise TypeError(f"Unsupported operand type(s) for +: 'CustomList' and '{type(other).__name__}'")

    def __radd__(self, other):
        return self + other

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return CustomList([i - other for i in self])
        elif isinstance(other, list):
            max_len = max(len(other), len(self))
            res = [0] * max_len
            for i in range(max_len):
                if i >= len(self):
                    res[i] -= other[i]
                elif i >= len(other):
                    res[i] = self[i]
                else:
                    res[i] = self[i] - other[i]
            return CustomList(res)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: 'CustomList' and '{type(other).__name__}")

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return CustomList([other - i for i in self])
        elif isinstance(other, list):
            max_len = max(len(other), len(self))
            res = [0] * max_len
            for i in range(max_len):
                if i >= len(other):
                    res[i] -= self[i]
                elif i >= len(self):
                    res[i] = other[i]
                else:
                    res[i] = other[i] - self[i]
            return CustomList(res)
        else:
            raise TypeError(f"Unsupported operand type(s) for -: '{type(other).__name__}' and 'CustomList'")

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










if __name__ == '__main__':
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

