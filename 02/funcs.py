from retry_deco import retry_deco


@retry_deco(3)
def add(a, b):
    return a + b


add(4, 2)
add(4, b=3)


@retry_deco(3)
def check_str(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, str)


check_str(value="123")
check_str(value=1)
# check_str(value=None)


@retry_deco(2, [ValueError])
def check_int(value=None):
    if value is None:
        raise ValueError()
    return isinstance(value, int)


check_int(value=1)
# check_int(value=None)

# def test_function(should_fail=False):
#     if should_fail:
#         raise CustomError("This is a custom error.")
#     return "Success!"
