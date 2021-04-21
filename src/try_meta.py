from functools import wraps
from pydoc import locate


def dec(ret=None, **kwargs):
    expected_args = [locate(kwargs.get(x)) for x in kwargs]
    expected_return_type = locate(ret)

    def callable(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            got_args = [type(x) for x in args]
            assert expected_args == got_args, f"expected args {expected_args}, got {got_args}"
            result = func(*args, **kwargs)
            assert type(
                result) == expected_return_type, f"expected return type {expected_return_type}, got {type(result)}"
            return result

        return wrapped

    return callable


@dec(ret="int", x="int", y="int")
def sum(x, y):
    return str(x + y)


def main():
    a = sum(3, 5)
    # b = sum('str1', 'str')


if __name__ == '__main__':
    main()
