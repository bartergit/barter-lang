from functools import wraps
from pydoc import locate
from collections.abc import Iterable


def define_type(el):
    if isinstance(el, Iterable) and type(el) is not str:
        return type(el)([define_type(x) for x in el])
    else:
        return type(el)


def define_locate(el):
    if isinstance(el, Iterable) and type(el) is not str:
        return type(el)([define_locate(x) for x in el])
    else:
        return locate(el)


def dec(ret=None, **kwargs):
    expected_args = [locate(kwargs.get(x)) for x in kwargs]
    expected_return_type = locate(ret)

    def callable(func):
        @wraps(func)
        def wrapped(*args, **kwargs):
            got_args = [type(x) for x in args]
            assert expected_args == got_args, f"expected args {expected_args}, got {got_args}"
            result = func(*args, **kwargs)
            assert type(result) == expected_return_type, \
                f"expected return type {expected_return_type}, got {type(result)}"
            return result

        return wrapped

    return callable


@dec(ret="int", x="int", y="int")
def sum(x, y):
    return x + y


def main():
    a = sum(3, 5)
    print(define_type([3, 5, {True, False}]))
    print(define_locate(['int', 'int', ('int', 'str')]))
    # print(define_type(['define',{2,1}]))
    # b = sum('str1', 'str')


if __name__ == '__main__':
    main()
