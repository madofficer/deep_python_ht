import unittest
from typing import assert_never

from descriptors import BaseDescriptor, Integer, String, PositiveInteger, Data


class TestDescriptors(unittest.TestCase):

    def setUp(self):
        self.data = Data(1, "Test Item", 100)

    def test_valid_data(self):
        self.assertEqual(self.data.num, 1)
        self.assertEqual(self.data.name, "Test Item")
        self.assertEqual(self.data.price, 100)

    def test_set_valid_values(self):
        self.data.num = 2
        self.data.name = "Updated Item"
        self.data.price = 150
        self.assertEqual(self.data.num, 2)
        self.assertEqual(self.data.name, "Updated Item")
        self.assertEqual(self.data.price, 150)

    def test_set_invalid_integer(self):
        with self.assertRaises(ValueError) as context:
            self.data.num = "not an integer"
        self.assertEqual(str(context.exception),
                         "Expected integer for 'num', got str")

        self.assertEqual(self.data.num, 1)
        try:
            self.data.num = "invalid_value"
        except ValueError:
            pass

    def test_set_invalid_string(self):
        with self.assertRaises(ValueError) as context:
            self.data.name = 12345
        self.assertEqual(str(context.exception),
                         "Expected string for 'name', got int")

        self.assertEqual(self.data.name, "Test Item")

    def test_set_negative_price(self):
        with self.assertRaises(ValueError) as context:
            self.data.price = -50
        self.assertEqual(str(context.exception),
                         "Expected positive integer for 'price', got -50")
        self.assertEqual(self.data.price, 100)

    def test_set_zero_price(self):
        with self.assertRaises(ValueError) as context:
            self.data.price = 0
        self.assertEqual(str(context.exception),
                         "Expected positive integer for 'price', got 0")

    def test_values_after_modifying_another_instance(self):
        data2 = Data(10, "Product", 200)

        data2.name = "New Product"
        self.assertEqual(data2.name, "New Product")

        self.assertEqual(self.data.name, "Test Item")

    def test_delete_attribute(self):
        with self.assertRaises(AttributeError) as context:
            del self.data.num
        self.assertEqual(str(context.exception),
                         "Can't delete attribute 'num'")

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError) as context:
            Data("not an integer", "Test Item", 100)
        self.assertEqual(str(context.exception),
                         "Expected integer for 'num', got str")

        with self.assertRaises(ValueError) as context:
            Data(1, 12345, 100)
        self.assertEqual(str(context.exception),
                         "Expected string for 'name', got int")

        with self.assertRaises(ValueError) as context:
            Data(1, "Test Item", -10)
        self.assertEqual(str(context.exception),
                         "Expected positive integer for 'price', got -10")

    def test_reassigning_valid_values(self):
        self.data.num = 5
        self.data.name = "Another Item"
        self.data.price = 250
        self.data.num = 10
        self.data.name = "Updated Again"
        self.data.price = 300
        self.assertEqual(self.data.num, 10)
        self.assertEqual(self.data.name, "Updated Again")
        self.assertEqual(self.data.price, 300)

    def test_independence(self):
        data1 = Data(5, "Item1", 100)
        data2 = Data(10, "Item2", 200)

        data1.num = 15
        data2.num = 20

        self.assertEqual(data1.num, 15)
        self.assertEqual(data2.num, 20)

    def test_base_validate(self):
        descriptor = BaseDescriptor()
        with self.assertRaises(NotImplementedError) as context:
            descriptor.validate("not valid")
        self.assertEqual(
            str(context.exception),
            "Subclasses must implement 'validate' method"
        )

    def test_custom_descriptor_without_validation(self):
        class CustomDescriptor(BaseDescriptor):
            pass

        class CustomData1:
            custom_field = CustomDescriptor()

        with self.assertRaises(NotImplementedError) as context:
            data1 = CustomData1()
            data1.custom_field = "some_value"
        self.assertEqual(
            str(context.exception),
            "Subclasses must implement 'validate' method"
        )
        with self.assertRaises(KeyError):
            self.assertFalse(data1.custom_field)

    def test_get(self):
        descriptor = Integer()
        result = descriptor.__get__(None, Data)
        self.assertIs(result, descriptor)


if __name__ == '__main__':
    unittest.main()
