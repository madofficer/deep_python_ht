import unittest
from unittest.mock import patch
from io import StringIO
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def setUp(self):
        self.a_custom = CustomList([5, 1, 3, 7])
        self.a_list = [5, 1, 3, 7]
        self.b_custom = CustomList([1, 2, 7])
        self.b_list = [1, 2, 7]


    def test_custom_list_init(self):
        self.assertIsInstance(CustomList(), CustomList)
        self.assertIsInstance(CustomList(self.a_list), CustomList)
        self.assertIsInstance(CustomList(tuple(self.b_list)), CustomList)
        self.assertIsInstance(CustomList(set(self.a_list)), CustomList)
        self.assertIsInstance(CustomList(frozenset(self.a_list)), CustomList)
        self.assertIsInstance(CustomList({1: 123, 2: 321}), CustomList)

    def test_custom_list_init_invalid(self):
        with self.assertRaises(TypeError):
            CustomList(124)
        with self.assertRaises(TypeError):
            CustomList('352')
        with self.assertRaises(TypeError):
            CustomList([1, 2, '3'])
        with self.assertRaises(TypeError):
            CustomList(((), 1))
        with self.assertRaises(TypeError):
            CustomList({1: 56, '2': 52})


    @patch('sys.stdout', new_callable=StringIO)
    def test_str_custom(self, mock_stdout):
        print(self.a_custom)
        self.assertEqual(mock_stdout.getvalue().strip(),
                         f'{self.a_list} = {sum(self.a_list)}')


    def test_add_int_pos(self):
        res = self.a_custom + 10
        self.assertEqual(res, CustomList([15, 11, 13, 17]))
        res = self.a_custom + 97
        self.assertEqual(res, CustomList([102, 98, 100, 104]))

    def test_add_int_non_pos(self):
        res = self.a_custom + 0
        self.assertEqual(res, self.a_custom)
        res = self.a_custom + (-1)
        self.assertEqual(res, CustomList([4, 0, 2, 6]))
        res = self.b_custom + (-52)
        self.assertEqual(res, CustomList([-51, -50, -45]))

    def test_add_float_pos(self):
        res = self.a_custom + .67
        self.assertEqual(res, CustomList([5.67, 1.67, 3.67, 7.67]))
        res = self.b_custom + 1.51
        self.assertEqual(res, CustomList([2.51, 3.51, 8.51]))

    def test_add_float_non_pos(self):
        res = self.a_custom + 0.0
        self.assertEqual(res, self.a_custom)
        res = self.b_custom + (-0.17)
        self.assertEqual(res, CustomList([.83, 1.83, 6.83]))

    def test_add_list(self):
        res = self.a_custom + self.a_list
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = self.a_custom + self.b_list
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = self.a_custom + [0, 1]
        self.assertEqual(res, CustomList([5, 2, 3, 7]))

    def test_add_custom_list(self):
        res = self.a_custom + CustomList([])
        self.assertEqual(res, self.a_custom)
        res = self.a_custom + self.b_custom
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = self.a_custom + CustomList([1, 2])
        self.assertEqual(res, CustomList([6, 3, 3, 7]))
        res = self.b_custom + CustomList([.4])
        self.assertEqual(res, CustomList([1.4, 2, 7]))

    # def test_add_invalid(self):



if __name__ == '__main__':
    unittest.main()
