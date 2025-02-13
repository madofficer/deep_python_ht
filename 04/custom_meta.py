class CustomMeta(type):
    def __new__(mcs, name, bases, attrs):
        new_attrs = {}
        for attr_name, attr_value in attrs.items():
            if not (attr_name.startswith("__") and attr_name.endswith("__")):
                new_attrs[f"custom_{attr_name}"] = attr_value
            else:
                new_attrs[attr_name] = attr_value

        cls_obj = super().__new__(mcs, name, bases, new_attrs)

        def custom_setattr(self, key, value):
            if not (key.startswith("__") and key.endswith("__")):
                renamed_key = f"custom_{key}"
                super(cls_obj, self).__setattr__(renamed_key, value)
            else:
                raise AttributeError(
                    f"Unable to customize magic method '{key}' "
                )

        cls_obj.__setattr__ = custom_setattr

        return cls_obj


class CustomClass(metaclass=CustomMeta):
    x = 50
    attr1 = "val1"
    _protected_attr = "protected_val"
    __private_attr = "private_val"

    def __init__(self, val=99):
        self.val = val

    def line(self):
        return 100

    def _protected_line(self):
        return 200

    def __private_line(self):
        return 300

    def __str__(self):
        return "Custom_by_metaclass"


# if __name__ == "__main__":
#     ex = CustomClass()
#     ex.custom_line()
#     print(ex.custom_line())
#     print(ex)
#     ex.n_attr = 100
#     print(ex.custom_n_attr)
#     print(ex.custom_x)
#     print(str(ex))
#     ex.__newAttr = 52
#     ex._n_attr = 100
#     print(ex.custom__CustomClass__private_line())
#     ex.__setattr__ = 5
#     # ex.__setattr__(s, 12)
#     print(ex.__dict__)
