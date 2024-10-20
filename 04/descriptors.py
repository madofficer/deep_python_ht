class BaseDescriptor:
    def __init__(self, name=None):
        self.name = name

    def __set_name__(self, owner, name):
        self.name = name

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return instance.__dict__[self.name]

    def __set__(self, instance, value):
        self.validate(value)
        instance.__dict__[self.name] = value

    def __delete__(self, instance):
        raise AttributeError(f"Can't delete attribute '{self.name}'")

    def validate(self, value):
        raise NotImplementedError("Subclasses must implement 'validate' method")


class Integer(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, int):
            raise ValueError(f"Expected integer for '{self.name}', "
                             f"got {type(value).__name__}")


class String(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected string for '{self.name}', "
                             f"got {type(value).__name__}")


class PositiveInteger(Integer):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(f"Expected positive integer for "
                             f"'{self.name}', got {value}")


class Data:
    num = Integer("num")
    name = String("name")
    price = PositiveInteger("price")

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price


if __name__ == "__main__":
    d1 = Data(5, "Item", 100)
    d2 = Data(10, "Product", 200)

    assert d1.num == 5
    assert d1.name == "Item"
    assert d1.price == 100

    d2.name = "New Product"
    assert d2.name == "New Product"
    # Убедитесь, что значения d1 не изменились
    assert d1.name == "Item"
