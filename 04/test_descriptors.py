import unittest
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
        self.assertEqual(str(context.exception), "Expected integer for 'num', got str")

    def test_set_invalid_string(self):
        with self.assertRaises(ValueError) as context:
            self.data.name = 12345
        self.assertEqual(str(context.exception), "Expected string for 'name', got int")

    def test_set_negative_price(self):
        with self.assertRaises(ValueError) as context:
            self.data.price = -50
        self.assertEqual(str(context.exception), "Expected positive integer for 'price', got -50")

    def test_set_zero_price(self):
        with self.assertRaises(ValueError) as context:
            self.data.price = 0
        self.assertEqual(str(context.exception), "Expected positive integer for 'price', got 0")

    def test_delete_attribute(self):
        with self.assertRaises(AttributeError) as context:
            del self.data.num
        self.assertEqual(str(context.exception), "Can't delete attribute 'num'")

    def test_invalid_initialization(self):
        with self.assertRaises(ValueError) as context:
            Data("not an integer", "Test Item", 100)
        self.assertEqual(str(context.exception), "Expected integer for 'num', got str")

        with self.assertRaises(ValueError) as context:
            Data(1, 12345, 100)
        self.assertEqual(str(context.exception), "Expected string for 'name', got int")

        with self.assertRaises(ValueError) as context:
            Data(1, "Test Item", -10)
        self.assertEqual(str(context.exception), "Expected positive integer for 'price', got -10")

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


if __name__ == '__main__':
    unittest.main()
