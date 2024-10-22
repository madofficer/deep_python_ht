import unittest
from io import StringIO
from copy import deepcopy
from operator import add, sub
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
        self.assertIsInstance(CustomList(iter([1, 2, 3])), CustomList)
        self.assertEqual(CustomList(iter([1, 2, 3])), CustomList([1, 2, 3]))
        self.assertEqual(list(CustomList(iter([1, 2, 3]))), [1, 2, 3])

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

    def test_str_custom(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        self.assertEqual(str(a_custom), "[5, 1, 3, 7] = 16")

    def test_add_int_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 10
        ans = CustomList([i + 10 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + 97
        ans = CustomList([i + 97 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_add_int_non_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 0
        ans = CustomList([i + 0 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + (-1)
        ans = CustomList([i + (-1) for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)
        res = b_custom + (-52)
        ans = CustomList([i + (-52) for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_float_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        res = a_custom + 0.67
        ans = CustomList([i + 0.67 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList([1, 2, 7])
        res = b_custom + 1.51
        ans = CustomList([i + 1.51 for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_float_non_pos(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()

        res = a_custom + 0.0
        ans = CustomList([i + 0.0 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList([1, 2, 7])

        res = b_custom + (-0.17)
        ans = CustomList([i + (-0.17) for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_add_list(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        a1 = a.copy()
        b = [1, 2, 7]
        b1 = b.copy()

        res = a_custom + a
        ans = CustomList(list(map(add, a, a)))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b
        ans = CustomList([i + j for i, j in zip_longest(a, b, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b, b1)
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + [0, 1]
        ans = CustomList([
            i + j for i, j in zip_longest(a, [0, 1], fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a))

    def test_add_tuple(self):
        a = (5, 1, 3, 7)
        a1 = deepcopy(a)
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)

        res = a_custom + a
        ans = CustomList(tuple(map(add, list(a), list(a))))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a, a1)
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b
        ans = CustomList([
            i + j for i, j in zip_longest(list(a), list(b), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))
        self.assertEqual(b, b1)

        res = a_custom + (0, 1)
        ans = CustomList([
            i + j for i, j in zip_longest(list(a), [0, 1], fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_add_custom_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a_custom + CustomList([])
        ans = CustomList([i + j for i, j in zip_longest(a, [], fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom + b_custom
        ans = CustomList([i + j for i, j in zip_longest(a, b, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(CustomList(a), CustomList(a1))
        self.assertEqual(CustomList(b), CustomList(b1))

        res = a_custom + CustomList([1, 2])
        ans = CustomList([
            i + j for i, j in zip_longest(a, [1, 2], fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(CustomList(a), CustomList(a1))

        res = b_custom + CustomList([0.4])
        ans = CustomList([1.4, 2, 7])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(CustomList(a), CustomList(a1))

    def test_add_invalid(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b_custom = CustomList(b)

        with self.assertRaises(TypeError):
            res = a_custom + "564"
        with self.assertRaises(TypeError):
            res = b_custom + (5, ())
        with self.assertRaises(TypeError):
            res = a_custom + {1, 77, 245}
        with self.assertRaises(TypeError):
            res = b_custom + {1: 2, 2: 2}
        with self.assertRaises(TypeError):
            res = b_custom + [(0, 0), {}, [1, 2]]
            print(res)

    def test_radd_int_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)

        res = 11 + a_custom
        ans = CustomList([11 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = 100 + a_custom
        ans = CustomList([100 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_radd_int_non_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = 0 + a_custom
        ans = CustomList([0 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = (-2) + a_custom
        ans = CustomList([-2 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = (-50) + b_custom
        ans = CustomList([-50 + i for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_float_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = 0.5 + a_custom
        ans = CustomList([0.5 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = 2.1 + b_custom
        ans = CustomList([3.1, 4.1, 9.1])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_float_non_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = 0.0 + a_custom
        ans = CustomList([0.0 + i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = -10.2 + b_custom
        ans = CustomList([-9.2, -8.2, -3.2])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a + a_custom
        ans = CustomList(list(map(add, a, a)))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a, a1)
        self.assertEqual(a_custom, CustomList(a1))

        res = b + a_custom
        ans = CustomList([i + j for i, j in zip_longest(a, b, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b, b1)
        self.assertEqual(b_custom, CustomList(b1))

        res = [0, 1] + a_custom
        ans = CustomList([
            i + j for i, j in zip_longest([0, 1], a, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_radd_tuple(self):
        a = (5, 1, 3, 7)
        a1 = deepcopy(a)
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)
        b_custom = CustomList(b)

        res = a + a_custom
        ans = CustomList(list(map(add, a, a)))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a, a1)
        self.assertEqual(a_custom, CustomList(a1))

        res = b + a_custom
        ans = CustomList([
            i + j for i, j in zip_longest(list(a), list(b), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b, b1)
        self.assertEqual(a_custom, CustomList(a1))

        res = (1, 0) + b_custom
        ans = CustomList([
            i + j for i, j in zip_longest([1, 0], list(b), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_radd_custom_list(self):
        a = (5, 1, 3, 7)
        a1 = deepcopy(a)
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)
        b_custom = CustomList(b)

        res = CustomList([]) + a_custom
        ans = CustomList([
            i + j for i, j in zip_longest([], list(a), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = b_custom + a_custom
        ans = CustomList([
            i + j for i, j in zip_longest(list(b), list(a), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))
        self.assertEqual(b_custom, CustomList(b1))

        res = CustomList([1, 2]) + a_custom
        ans = CustomList([
            i + j for i, j in zip_longest([1, 2], list(a), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = CustomList([0.4, 1]) + b_custom
        ans = CustomList(
            [i + j for i, j in zip_longest([0.4, 1], list(b), fillvalue=0)]
        )
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))

        res = [] + CustomList([])
        ans = CustomList(list(map(add, [], [])))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))

    def test_radd_invalid(self):
        a = (5, 1, 3, 7)
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b_custom = CustomList(b)

        with self.assertRaises(TypeError):
            res = "" + a_custom
        with self.assertRaises(TypeError):
            res = ({5}, 5) + b_custom
        with self.assertRaises(TypeError):
            res = {1, 11, 111} + a_custom
        with self.assertRaises(TypeError):
            res = {1: 2, 2: 2} + b_custom
        with self.assertRaises(TypeError):
            res = [(0, 0), {22, 31}, []] + b_custom
            print(res)

    def test_sub_int_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a_custom - 1
        ans = CustomList([i - 1 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = b_custom - 10
        ans = CustomList([i - 10 for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_sub_int_non_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a_custom - 0
        ans = CustomList([i - 0 for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = a_custom - (-1)
        ans = CustomList([i - (-1) for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = b_custom - (-42)
        ans = CustomList([i - (-42) for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_sub_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = a_custom - b
        ans = CustomList([
            i - j for i, j in zip_longest(a, b, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b, b1)
        self.assertEqual(a_custom, CustomList(a1))

        c = [0, 1, 3, -4.5]
        c1 = c.copy()
        res = b_custom - c
        ans = CustomList([
            i - j for i, j in zip_longest(b, c, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(c, c1)
        self.assertEqual(b_custom, CustomList(b1))

        res = a_custom - [1, 1]
        ans = CustomList([
            i - j for i, j in zip_longest(a, [1, 1], fillvalue=0)
                          ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_sub_custom_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)
        b_custom = CustomList(b)

        res = a_custom - b
        ans = CustomList([
            i - j for i, j in zip_longest(a, b, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))
        self.assertEqual(b, b1)

        c = (0, 1, 3, -4.5)
        c1 = deepcopy(c)
        res = b_custom - c
        ans = CustomList([
            i - j for i, j in zip_longest(list(b), list(c), fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))
        self.assertEqual(c, c1)

        res = a_custom - (1, 1)
        ans = CustomList([
            i - j for i, j in zip_longest(a, [1, 1], fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_sub_invalid(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b_custom = CustomList(b)

        with self.assertRaises(TypeError):
            res = a_custom - "564"
        with self.assertRaises(TypeError):
            res = b_custom - (5, ())
            print(res)

    def test_rsub_int_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)
        b_custom = CustomList(b)

        res = 10 - a_custom
        ans = CustomList([10 - i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = 15 - b_custom
        ans = CustomList([15 - i for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_rsub_int_non_pos(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = (1, 2, 7)
        b1 = deepcopy(b)
        b_custom = CustomList(b)

        res = 0 - a_custom
        ans = CustomList([0 - i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = -5 - a_custom
        ans = CustomList([-5 - i for i in a])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = -100 - b_custom
        ans = CustomList([-100 - i for i in b])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

    def test_rsub_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = [10, 10] - a_custom
        ans = CustomList([
            i - j for i, j in zip_longest([10, 10], a, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = [10, 10, 10] - b_custom
        ans = CustomList(list(map(sub, [10, 10, 10], b)))
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b_custom, CustomList(b1))

        res = [1] - a_custom
        ans = CustomList([i - j for i, j in zip_longest([1], a, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

    def test_rsub_custom_list(self):
        a = [5, 1, 3, 7]
        a1 = a.copy()
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b1 = b.copy()
        b_custom = CustomList(b)

        res = b - a_custom
        ans = CustomList([i - j for i, j in zip_longest(b, a, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(b, b1)
        self.assertEqual(a_custom, CustomList(a1))

        res = a - b_custom
        ans = CustomList([i - j for i, j in zip_longest(a, b, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a, a1)
        self.assertEqual(b_custom, CustomList(b1))

        res = (10, 20) - a_custom
        ans = CustomList([
            i - j for i, j in zip_longest([10, 20], a, fillvalue=0)
        ])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = [] - a_custom
        ans = CustomList([i - j for i, j in zip_longest([], a, fillvalue=0)])
        self.assertEqual(res, ans)
        self.assertEqual(list(res), list(ans))
        self.assertEqual(a_custom, CustomList(a1))

        res = [] - CustomList([])
        ans = CustomList([])
        self.assertEqual(res, CustomList(list(map(sub, [], []))))
        self.assertEqual(list(res), list(ans))

    def test_rsub_invalid(self):
        a = [5, 1, 3, 7]
        a_custom = CustomList(a)
        b = [1, 2, 7]
        b_custom = CustomList(b)

        with self.assertRaises(TypeError):
            res = "test_string" - a_custom
        with self.assertRaises(TypeError):
            res = (5, "str") - b_custom
        with self.assertRaises(TypeError):
            res = {1, 2, 3} - a_custom
        with self.assertRaises(TypeError):
            res = {1: 2, 3: 4} - b_custom
        with self.assertRaises(TypeError):
            res = [(5, 6), {}] - b_custom
            print(res)

    def test_eq_operator(self):

        self.assertTrue(CustomList([5, 1, 3, 7]) == CustomList((7, 3, 5, 1)))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([1, 2, 7]))
        self.assertTrue(CustomList([5, 1, 3, 7]) == CustomList((5, 1, 10)))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([10, 10, 10]))
        self.assertFalse(CustomList([5, 1, 3, 7]) == CustomList([]))

    def test_ne_operator(self):
        self.assertTrue(CustomList([5, 1, 3, 7.1]) != CustomList([1, 2, 7]))
        self.assertTrue(
            CustomList([5, 1.0, 3, 7]) == CustomList({5, 1, 10})
        )
        self.assertTrue(CustomList([5, 1, 3, 7]) != CustomList([10, 10, 10]))
        self.assertFalse(
            CustomList([5, 1.0, 3, 7]) != CustomList([5, 1, 3.0, 7])
        )
        self.assertTrue(CustomList([5, 1, 3, 7.12]) != CustomList([]))

    def test_gt_operator(self):
        self.assertTrue(CustomList([5, 1, 3.2, 8]) > CustomList([1, 2, 7]))
        self.assertFalse(
            CustomList([5, 1.24, 3, 7.9]) > CustomList([23.45, 1.0])
        )

        self.assertTrue(CustomList([5, 1, 3.33, 7]) > CustomList([1, 1, 1]))
        self.assertFalse(CustomList([5, 1, 5, 7]) > CustomList([10.1, 10, 10]))
        self.assertTrue(CustomList([4.01, 1, 8.2, 7]) > CustomList([]))

    def test_ge_operator(self):
        self.assertTrue(
            CustomList([5, 1, 0, 77]) >= CustomList((2.4, 0, 1, 0.5))
        )
        self.assertFalse(CustomList([2, 4, 3, 9]) >= CustomList((111.2,)))

        self.assertTrue(CustomList([9, 1, 7, 8]) >= CustomList([5, 1, 3, 7]))
        self.assertFalse(CustomList([7, 3, 4, 7]) >= CustomList([10, 10, 10]))
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
