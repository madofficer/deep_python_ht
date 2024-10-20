import unittest
from unittest.mock import patch
from io import StringIO
from copy import deepcopy
from operator import add
from itertools import zip_longest
from custom_list import CustomList


class TestCustomList(unittest.TestCase):

    def test_custom_list_init(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        b = (1, 2, 7)
        b1 = deepcopy(b)
        self.assertIsInstance(CustomList(), CustomList)
        self.assertIsInstance(CustomList(a), CustomList)
        self.assertEqual(a, a1)

        self.assertIsInstance(CustomList(b), CustomList)
        self.assertEqual(b, b1)

        self.assertIsInstance(CustomList(set(a)), CustomList)
        self.assertIsInstance(CustomList(frozenset(a)), CustomList)

        self.assertIsInstance(CustomList({1: 123, 2: 321}), CustomList)
        self.assertIsInstance(CustomList(range(1, 11)), CustomList)
        self.assertIsInstance(CustomList(i for i in range(13)), CustomList)

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
        print(CustomList([5, 1, 3, 7]))
        self.assertEqual(mock_stdout.getvalue().strip(),
                         str(CustomList([5, 1, 3, 7])))

    def test_add_int_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 10
        self.assertEqual(res, CustomList([i + 10 for i in a]))
        self.assertEqual(a_custom, CustomList(a1))
        res = a_custom + 97
        self.assertEqual(res, CustomList([i + 97 for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

    def test_add_int_non_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 0
        self.assertEqual(res, CustomList([i + 0 for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + (-1)
        self.assertEqual(res, CustomList([i + (-1) for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)
        res = b_custom + (-52)
        self.assertEqual(res, CustomList([i + (-52) for i in b]))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_float_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 0.67
        self.assertEqual(res, CustomList([i + 0.67 for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList([1, 2, 7])
        res = b_custom + 1.51
        self.assertEqual(res, CustomList([i + 1.51 for i in b]))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_float_non_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 0.0
        self.assertEqual(res, CustomList([i + 0.0 for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList([1, 2, 7])

        res = b_custom + (-0.17)
        self.assertEqual(res, CustomList([i + (-0.17) for i in b]))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_list(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        b = [1, 2, 7]
        b1 = b.copy()

        res = a_custom + a
        self.assertEqual(res, CustomList(list(map(add, a, a))))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b
        self.assertEqual(
            res, CustomList([i + j for i, j in zip_longest(a, b, fillvalue=0)])
        )
        self.assertEqual(b, b1)
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + [0, 1]
        self.assertEqual(
            res, CustomList([
                i + j for i, j in zip_longest(a, [0, 1], fillvalue=0)
            ])
        )
        self.assertEqual(a_custom, CustomList(a))

    def test_add_tuple(self):
        a = (5, 1, 3, 7)
        a1 = deepcopy(a)
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)

        res = a_custom + a
        self.assertEqual(res, CustomList(tuple(map(add, list(a), list(a)))))
        self.assertEqual(a, a1)
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b
        self.assertEqual(
            res,
            CustomList([
                i + j for i, j in zip_longest(list(a), list(b), fillvalue=0)
            ]),
        )
        self.assertEqual(a_custom, CustomList(a1))
        self.assertEqual(b, b1)

        res = a_custom + (0, 1)
        self.assertEqual(
            res,
            CustomList([
                i + j for i, j in zip_longest(list(a), [0, 1], fillvalue=0)
            ]),
        )
        self.assertEqual(a_custom, CustomList(a1))

    def test_add_custom_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a_custom + CustomList([])
        self.assertEqual(
            res, CustomList([i + j for i, j in zip_longest(a, [], fillvalue=0)])
        )
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b_custom
        self.assertEqual(
            res, CustomList([i + j for i, j in zip_longest(a, b, fillvalue=0)])
        )
        self.assertEqual(CustomList(a), CustomList(a1))
        self.assertEqual(CustomList(b), CustomList(b1))

        res = a_custom + CustomList([1, 2])
        self.assertEqual(
            res, CustomList([
                i + j for i, j in zip_longest(a, [1, 2], fillvalue=0)
            ])
        )
        self.assertEqual(CustomList(a), CustomList(a1))

        res = b_custom + CustomList([0.4])
        self.assertEqual(res, CustomList([1.4, 2, 7]))
        self.assertEqual(CustomList(a), CustomList(a1))

    def test_add_invalid(self):
        with self.assertRaises(TypeError):
            res = CustomList([5, 1, 3, 7]) + "564"
        with self.assertRaises(TypeError):
            res = CustomList([1, 2, 7]) + (5, ())
        with self.assertRaises(TypeError):
            res = CustomList([5, 1, 3, 7]) + {1, 77, 245}
        with self.assertRaises(TypeError):
            res = CustomList([1, 2, 7]) + {1: 2, 2: 2}
        with self.assertRaises(TypeError):
            res = CustomList([1, 2, 7]) + [(0, 0), {}, [1, 2]]
            print(res)

    def test_radd_int_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)

        res = 11 + a_custom
        self.assertEqual(res, CustomList([11 + i for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        res = 100 + a_custom
        self.assertEqual(res, CustomList([100 + i for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

    def test_radd_int_non_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = 0 + a_custom
        self.assertEqual(res, CustomList([0 + i for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        res = (-2) + a_custom
        self.assertEqual(res, CustomList([-2 + i for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        res = (-50) + b_custom
        self.assertEqual(res, CustomList([-50 + i for i in b]))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_float_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = 0.5 + a_custom
        self.assertEqual(res, CustomList([0.5 + i for i in a]))
        self.assertEqual(a_custom, CustomList(a1))

        res = 2.1 + b_custom
        self.assertEqual(res, CustomList([3.1, 4.1, 9.1]))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_float_non_pos(self):
        res = 0.0 + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 1, 3, 7]))
        res = -10.2 + CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([-9.2, -8.2, -3.2]))

    def test_radd_list(self):
        res = [5, 1, 3, 7] + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = [1, 2, 7] + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = [0, 1] + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 2, 3, 7]))

    def test_radd_tuple(self):
        res = tuple([5, 1, 3, 7]) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([10, 2, 6, 14]))
        res = tuple([1, 2, 7]) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = (1, 0) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([6, 1, 3, 7]))

    def test_radd_custom_list(self):
        res = CustomList([]) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 1, 3, 7]))
        res = CustomList([1, 2, 7]) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([6, 3, 10, 7]))
        res = CustomList([1, 2]) + CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([6, 3, 3, 7]))
        res = CustomList([0.4, 1]) + CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([1.4, 3, 7]))

    def test_radd_invalid(self):
        with self.assertRaises(TypeError):
            res = "" + CustomList([5, 1, 3, 7])
        with self.assertRaises(TypeError):
            res = ({5}, 5) + CustomList([1, 2, 7])
        with self.assertRaises(TypeError):
            res = {1, 11, 111} + CustomList([5, 1, 3, 7])
        with self.assertRaises(TypeError):
            res = {1: 2, 2: 2} + CustomList([1, 2, 7])
        with self.assertRaises(TypeError):
            res = [(0, 0), {22, 31}, []] + CustomList([1, 2, 7])
            print(res)

    def test_sub_int_pos(self):
        res = CustomList([5, 1, 3, 7]) - 1
        self.assertEqual(res, CustomList([4, 0, 2, 6]))
        res = CustomList([1, 2, 7]) - 10
        self.assertEqual(res, CustomList((-9, -8, -3)))

    def test_sub_int_non_pos(self):
        res = CustomList([5, 1, 3, 7]) - 0
        self.assertEqual(res, CustomList([5, 1, 3, 7]))
        res = CustomList([5, 1, 3, 7]) - (-1)
        self.assertEqual(res, CustomList([6, 2, 4, 8]))
        res = CustomList([1, 2, 7]) - (-42)
        self.assertEqual(res, CustomList((43, 44, 49)))

    def test_sub_list(self):
        res = CustomList([5, 1, 3, 7]) - [1, 2, 7]
        self.assertEqual(res, CustomList([4, -1, -4, 7]))
        res = CustomList([1, 2, 7]) - [0, 1, 3, -4.5]
        self.assertEqual(res, CustomList([1, 1, 4, 4.5]))
        res = CustomList([5, 1, 3, 7]) - [1, 1]
        self.assertEqual(res, CustomList([4, 0, 3, 7]))

    def test_sub_custom_list(self):
        res = CustomList([5, 1, 3, 7]) - tuple([1, 2, 7])
        self.assertEqual(res, CustomList([4, -1, -4, 7]))
        res = CustomList([1, 2, 7]) - (0, 1, 3, -4.5)
        self.assertEqual(res, CustomList([1, 1, 4, 4.5]))
        res = CustomList([5, 1, 3, 7]) - (1, 1)
        self.assertEqual(res, CustomList([4, 0, 3, 7]))

    def test_sub_invalid(self):
        with self.assertRaises(TypeError):
            res = CustomList([5, 1, 3, 7]) - "564"
        with self.assertRaises(TypeError):
            res = CustomList([1, 2, 7]) - (5, ())
            print(res)

    def test_rsub_int_pos(self):
        res = 10 - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 9, 7, 3]))
        res = 15 - CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([14, 13, 8]))

    def test_rsub_int_non_pos(self):
        res = 0 - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([-5, -1, -3, -7]))
        res = -5 - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([-10, -6, -8, -12]))
        res = -100 - CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([-101, -102, -107]))

    def test_rsub_list(self):
        res = [10, 10] - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 9, -3, -7]))
        res = [10, 10, 10] - CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([9, 8, 3]))
        res = [1] - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([-4, -1, -3, -7]))

    def test_rsub_custom_list(self):
        res = [1, 2, 7] - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([-4, 1, 4, -7]))
        res = [5, 1, 3, 7] - CustomList([1, 2, 7])
        self.assertEqual(res, CustomList([4, -1, -4, 7]))
        res = (10, 20) - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([5, 19, -3, -7]))
        res = [] - CustomList([5, 1, 3, 7])
        self.assertEqual(res, CustomList([-5, -1, -3, -7]))
        res = [10, 20] - CustomList([])
        self.assertEqual(res, CustomList([10, 20]))

    def test_rsub_invalid(self):
        with self.assertRaises(TypeError):
            res = "test_string" - CustomList([5, 1, 3, 7])
        with self.assertRaises(TypeError):
            res = (5, "str") - CustomList([1, 2, 7])
        with self.assertRaises(TypeError):
            res = {1, 2, 3} - CustomList([5, 1, 3, 7])
        with self.assertRaises(TypeError):
            res = {1: 2, 3: 4} - CustomList([1, 2, 7])
        with self.assertRaises(TypeError):
            res = [(5, 6), {}] - CustomList([1, 2, 7])
            print(res)

    def test_eq_operator(self):

        self.assertTrue(CustomList([5, 1, 3, 7]) == CustomList((7, 3, 5, 1)))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([1, 2, 7]))
        self.assertTrue(CustomList([5, 1, 3, 7]) == CustomList((5, 1, 10)))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([10, 10, 10]))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([]))

    def test_ne_operator(self):
        self.assertTrue(CustomList([5, 1, 3, 7.1]) != CustomList([1, 2, 7]))
        self.assertTrue(CustomList([5, 1.0, 3, 7]) == CustomList({5, 1, 10}))
        self.assertTrue(CustomList([5, 1, 3, 7]) != CustomList([10, 10, 10]))
        self.assertFalse(
            CustomList([5, 1.0, 3, 7]) != CustomList([5, 1, 3.0, 7])
        )
        self.assertTrue(CustomList([5, 1, 3, 7.12]) != CustomList([]))

    def test_gt_operator(self):
        self.assertTrue(CustomList([5, 1, 3.2, 8]) > CustomList([1, 2, 7]))
        self.assertFalse(
            CustomList([5, 1.24, 3, 7.9]) > CustomList([23.45, 1.0]))

        self.assertTrue(CustomList([5, 1, 3.33, 7]) > CustomList([1, 1, 1])
                        )
        self.assertFalse(CustomList(
            [5, 1, 5, 7]) > CustomList([10.1, 10, 10])
                         )
        self.assertTrue(CustomList([4.01, 1, 8.2, 7]) > CustomList([]))

    def test_ge_operator(self):
        self.assertTrue(
            CustomList([5, 1, 0, 77]) >= CustomList((2.4, 0, 1, 0.5))
        )
        self.assertFalse(CustomList([2, 4, 3, 9]) >= CustomList((111.2,)))

        self.assertTrue(
            CustomList([9, 1, 7, 8]) >= CustomList([5, 1, 3, 7])
        )
        self.assertFalse(
            CustomList([7, 3, 4, 7]) >= CustomList([10, 10, 10])
        )
        self.assertTrue(CustomList([5, 5, 5, 8]) >= CustomList([]))

    def test_lt_operator(self):
        self.assertTrue(CustomList([1, 2, 7]) < CustomList([5, 1, 3, 7]))
        self.assertFalse(CustomList([1, 200]) < CustomList([5, 1, 3, 7]))
        self.assertTrue(CustomList([4, 1, 3, 7, 1]) < CustomList([10, 10, 10]))
        self.assertFalse(CustomList([6, 1, 3, 7]) < CustomList([1, 1, 1]))
        self.assertFalse(CustomList([5, 1, 3, 8]) < CustomList([]))

    def test_le_operator(self):
        self.assertTrue(
            CustomList([5, 1, 3, 7]) <= CustomList(({1: 1, 3: 3, 5: 5, 7: 0}))
        )
        self.assertTrue(CustomList([1, 2, 7]) <= CustomList([5, 1, 3, 7]))
        self.assertFalse(CustomList({53, 1000}) <= CustomList([5, 1, 3, 7]))
        self.assertTrue(CustomList([5, 1, 6, 7]) <= CustomList([10, 10, 10]))
        self.assertFalse(CustomList([5, 1, 5, 7, 9]) <= CustomList([1, 1, 1]))
        self.assertFalse(CustomList([5, 1, 3, 7, 4]) <= CustomList([]))


if __name__ == "__main__":
    unittest.main()
