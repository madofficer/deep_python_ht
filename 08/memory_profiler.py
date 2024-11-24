import weakref
import timeit


class Regular:
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3


class Slots:
    __slots__ = ("attr1", "attr2", "attr3")

    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3


class Weakref:
    def __init__(self, attr1, attr2, attr3):
        self.attr1 = attr1
        self.attr2 = attr2
        self.attr3 = attr3


def create_obj(Class, n):
    return [Class(i, i + 1, i + 2) for i in range(n)]


def modify(instances):
    for obj in instances:
        (
            obj.attr1,
            obj.attr2,
            obj.attr3,
        ) = (
            obj.attr2,
            obj.attr3,
            obj.attr1,
        )
        _ = obj.attr1, obj.attr2, obj.attr3


n = 10**7
classes = {"Regular": Regular, "Slots": Slots, "Weakref": Weakref}

for name, Class in classes.items():
    time = timeit.timeit(lambda: create_obj(Class, n))
    print(f"{name}: create {n} examples - {time:.2f} sec")


for name, Class in classes.items():
    instances = create_obj(Class, n)
    time = timeit.timeit(lambda: modify(instances))
    print(f"{name}: reading/modifying attrs - {time:.2f} sec")
