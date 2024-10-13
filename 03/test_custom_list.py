import unittest
from logging import setLogRecordFactory
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
            CustomList("352")
        with self.assertRaises(TypeError):
            CustomList([1, 2, "3"])
        with self.assertRaises(TypeError):
            CustomList(((), 1))
        with self.assertRaises(TypeError):
            CustomList({1: 56, "2": 52})

    @patch("sys.stdout", new_callable=StringIO)
    def test_str_custom(self, mock_stdout):
        print(self.a_custom)
        self.assertEqual(
            mock_stdout.getvalue().strip(),
    f"{self.a_list} = {sum(self.a_list)}"
        )

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
        res = self.a_custom + 0.67
        self.assertEqual(res, CustomList([5.67, 1.67, 3.67, 7.67]))
        res = self.b_custom + 1.51
        self.assertEqual(res, CustomList([2.51, 3.51, 8.51]))

    def test_add_float_non_pos(self):
        res = self.a_custom + 0.0
        self.assertEqual(res, self.a_custom)
        res = self.b_custom + (-0.17)
        self.assertEqual(res, CustomList([0.83, 1.83, 6.83]))

    def test_add_list(self):
        res = self.a_custom + self.a_list
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = self.a_custom + self.b_list
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = self.a_custom + [0, 1]
        self.assertEqual(res, CustomList([5, 2, 3, 7]))

    def test_add_tuple(self):
        res = self.a_custom + tuple(self.a_list)
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = self.a_custom + tuple(self.b_list)
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = self.a_custom + (0, 1)
        self.assertEqual(res, CustomList([5, 2, 3, 7]))

    def test_add_custom_list(self):
        res = self.a_custom + CustomList([])
        self.assertEqual(res, self.a_custom)
        res = self.a_custom + self.b_custom
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = self.a_custom + CustomList([1, 2])
        self.assertEqual(res, CustomList([6, 3, 3, 7]))
        res = self.b_custom + CustomList([0.4])
        self.assertEqual(res, CustomList([1.4, 2, 7]))

    def test_add_invalid(self):
        with self.assertRaises(TypeError):
            res = self.a_custom + "564"
        with self.assertRaises(TypeError):
            res = self.b_custom + (5, ())
        with self.assertRaises(TypeError):
            res = self.a_custom + {1, 77, 245}
        with self.assertRaises(TypeError):
            res = self.b_custom + {1: 2, 2: 2}
        with self.assertRaises(TypeError):
            res = self.b_custom + [(0, 0), {}, [1, 2]]
            print(res)

    def test_radd_int_pos(self):
        res = 11 + self.a_custom
        self.assertEqual(res, CustomList([16, 12, 14, 18]))
        res = 100 + self.a_custom
        self.assertEqual(res, CustomList([105, 101, 103, 107]))

    def test_radd_int_non_pos(self):
        res = 0 + self.a_custom
        self.assertEqual(res, self.a_custom)
        res = (-2) + self.a_custom
        self.assertEqual(res, CustomList([3, -1, 1, 5]))
        res = (-50) + self.b_custom
        self.assertEqual(res, CustomList([-49, -48, -43]))

    def test_radd_float_pos(self):
        res = 0.5 + self.a_custom
        self.assertEqual(res, CustomList([5.5, 1.5, 3.5, 7.5]))
        res = 2.1 + self.b_custom
        self.assertEqual(res, CustomList([3.1, 4.1, 9.1]))

    def test_radd_float_non_pos(self):
        res = 0.0 + self.a_custom
        self.assertEqual(res, self.a_custom)
        res = -10.2 + self.b_custom
        self.assertEqual(res, CustomList([-9.2, -8.2, -3.2]))

    def test_radd_list(self):
        res = self.a_list + self.a_custom
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = self.b_list + self.a_custom
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = [0, 1] + self.a_custom
        self.assertEqual(res, CustomList([5, 2, 3, 7]))

    def test_radd_tuple(self):
        res = tuple(self.a_list) + self.a_custom
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = tuple(self.b_list) + self.a_custom
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = (1, 0) + self.a_custom
        self.assertEqual(res, CustomList([6, 1, 3, 7]))

    def test_radd_custom_list(self):
        res = CustomList([]) + self.a_custom
        self.assertEqual(res, self.a_custom)
        res = self.b_custom + self.a_custom
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = CustomList([1, 2]) + self.a_custom
        self.assertEqual(res, CustomList([6, 3, 3, 7]))
        res = CustomList([0.4, 1]) + self.b_custom
        self.assertEqual(res, CustomList([1.4, 3, 7]))

    def test_radd_invalid(self):
        with self.assertRaises(TypeError):
            res = "" + self.a_custom
        with self.assertRaises(TypeError):
            res = ({5}, 5) + self.b_custom
        with self.assertRaises(TypeError):
            res = {1, 11, 111} + self.a_custom
        with self.assertRaises(TypeError):
            res = {1: 2, 2: 2} + self.b_custom
        with self.assertRaises(TypeError):
            res = [(0, 0), {22, 31}, []] + self.b_custom
            print(res)

    def test_sub_int_pos(self):
        res = self.a_custom - 1
        self.assertEqual(res, CustomList([4, 0, 2, 6]))
        res = self.b_custom - 10
        self.assertEqual(res, CustomList((-9, -8, -3)))

    def test_sub_int_non_pos(self):
        res = self.a_custom - 0
        self.assertEqual(res, self.a_custom)
        res = self.a_custom - (-1)
        self.assertEqual(res, CustomList([6, 2, 4, 8]))
        res = self.b_custom - (-42)
        self.assertEqual(res, CustomList((43, 44, 49)))

    def test_sub_list(self):
        res = self.a_custom - self.b_list
        self.assertEqual(res, CustomList([4, -1, -4, 7]))
        res = self.b_custom - [0, 1, 3, -4.5]
        self.assertEqual(res, CustomList([1, 1, 4, 4.5]))
        res = self.a_custom - [1, 1]
        self.assertEqual(res, CustomList([4, 0, 3, 7]))

    def test_sub_custom_list(self):
        res = self.a_custom - tuple(self.b_list)
        self.assertEqual(res, CustomList([4, -1, -4, 7]))
        res = self.b_custom - (0, 1, 3, -4.5)
        self.assertEqual(res, CustomList([1, 1, 4, 4.5]))
        res = self.a_custom - (1, 1)
        self.assertEqual(res, CustomList([4, 0, 3, 7]))


if __name__ == "__main__":
    unittest.main()
