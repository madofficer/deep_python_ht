class BaseDescriptor:
    def __init__(self, name=None):
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
            raise ValueError(f"Expected integer for '{self.name}', got {type(value).__name__}")


class String(BaseDescriptor):
    def validate(self, value):
        if not isinstance(value, str):
            raise ValueError(f"Expected string for '{self.name}', got {type(value).__name__}")


class PositiveInteger(Integer):
    def validate(self, value):
        super().validate(value)
        if value <= 0:
            raise ValueError(f"Expected positive integer for '{self.name}', got {value}")


class Data:
    num = Integer("num")
    name = String("name")
    price = PositiveInteger("price")

    def __init__(self, num, name, price):
        self.num = num
        self.name = name
        self.price = price

if __name__ == "__main__":
    data = Data(1, "Test Item", 100)
    print(data.num, data.name, data.price)
