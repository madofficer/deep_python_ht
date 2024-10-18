import unittest
from custom_meta import CustomMeta, CustomClass


class TestCustomMeta(unittest.TestCase):

    def setUp(self):
        self.obj = CustomClass(777)

    def test_custom_meta(self):
        self.assertTrue(issubclass(CustomMeta, type))
        self.assertTrue(isinstance(CustomClass, CustomMeta))

        class EmptyClass(metaclass=CustomMeta):
            pass

        empty = EmptyClass()
        self.assertTrue(isinstance(EmptyClass, CustomMeta))
        self.assertTrue(isinstance(empty, EmptyClass))

    def test_static_attrs(self):
        self.assertTrue(hasattr(CustomClass, "custom_x"))
        self.assertFalse(hasattr(CustomClass, "x"))
        self.assertEqual(CustomClass.custom_x, 50)
        with self.assertRaises(AttributeError):
            print(CustomClass.x)

        self.assertTrue(hasattr(CustomClass, "custom_attr1"))
        self.assertFalse(hasattr(CustomClass, "attr1"))
        self.assertEqual(CustomClass.custom_attr1, "val1")
        with self.assertRaises(AttributeError):
            print(CustomClass.attr1)

        self.assertTrue(hasattr(CustomClass, "custom__protected_attr"))
        self.assertFalse(hasattr(CustomClass, "_protected_attr"))
        self.assertEqual(CustomClass.custom__protected_attr, "protected_val")
        with self.assertRaises(AttributeError):
            print(CustomClass._protected_attr)

        self.assertTrue(hasattr(CustomClass, "custom__CustomClass__private_attr"))
        self.assertFalse(hasattr(CustomClass, "_CustomClass__private_attr"))
        self.assertEqual(CustomClass.custom__CustomClass__private_attr, "private_val")
        with self.assertRaises(AttributeError):
            print(CustomClass._CustomClass__protected_attr)

    def test_instance_attrs(self):
        self.assertTrue(hasattr(self.obj, "custom_val"))
        self.assertFalse(hasattr(self.obj, "val"))
        self.assertEqual(self.obj.custom_val, 777)
        with self.assertRaises(AttributeError):
            print(self.obj.val)

    def test_dynamic_attrs(self):
        self.obj.n_attr = 10
        self.assertTrue(hasattr(self.obj, "custom_n_attr"))
        self.assertFalse(hasattr(self.obj, "n_attr"))
        self.assertEqual(self.obj.custom_n_attr, 10)
        with self.assertRaises(AttributeError):
            print(self.obj.n_attr)

        self.obj._n_protected_attr = "new_protected"
        self.assertTrue(hasattr(self.obj, "custom__n_protected_attr"))
        self.assertFalse(hasattr(self.obj, "_n_protected_attr"))
        self.assertEqual(self.obj.custom__n_protected_attr, "new_protected")
        with self.assertRaises(AttributeError):
            print(self.obj._n_protected_attr)

        setattr(self.obj, "__non_private_attr", "private_but_not")
        self.assertTrue(hasattr(self.obj, "custom___non_private_attr"))
        self.assertFalse(hasattr(self.obj, "__non_private_attr"))
        self.assertFalse(hasattr(self.obj, "custom__CustomClass__non_private_attr"))
        with self.assertRaises(AttributeError):
            print(self.obj._CustomClass__non_private_attr)

    def test_magic_methods(self):
        self.assertEqual(str(self.obj), "Custom_by_metaclass")

    def test_regular_methods(self):
        self.assertTrue(hasattr(self.obj, "custom_line"))
        self.assertFalse(hasattr(self.obj, "line"))
        self.assertEqual(self.obj.custom_line(), 100)
        with self.assertRaises(AttributeError):
            print(self.obj.line())

        self.assertTrue(hasattr(self.obj, "custom__protected_line"))
        self.assertFalse(hasattr(self.obj, "_protected_line"))
        self.assertTrue(self.obj.custom__protected_line, 200)
        with self.assertRaises(AttributeError):
            print(self.obj.line())

        self.assertTrue(hasattr(self.obj, "custom__CustomClass__private_line"))
        self.assertFalse(hasattr(self.obj, "_CustomClass__private_line"))
        self.assertTrue(self.obj.custom__CustomClass__private_line, 200)
        with self.assertRaises(AttributeError):
            print(self.obj._CustomClass__private_line())


    def test_invalid_attr_name(self):
        with self.assertRaises(TypeError):
            setattr(self.obj, 123, "invalid_attr_name")


if __name__ == "__main__":
    unittest.main()
