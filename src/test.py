import datetime
from parse_ast import create_program
import sys
from colorama import init, Fore, Style

test_number = 0


def red(msg):
    return Fore.RED + msg + Style.RESET_ALL


def green(msg):
    return Fore.GREEN + msg + Style.RESET_ALL


def get_log():
    with open("build/log.txt", "r") as f:
        return f.read().split()


def get_file(name):
    with open(f"test/{name}.barter", "r") as f:
        return f.read()


def clear_log():
    with open("build/log.txt", "w") as f:
        f.write("")
        return


def run_program(name):
    create_program(get_file(name), name, True, False)


class Test:
    def __init__(self):
        self.start = None

    def equal(self, one, two, name=None, msg=None):
        global test_number
        if name:
            test_name = f"'{name}'"
        else:
            test_name = test_number
            test_number += 1
        test_name += (25 - len(test_name))*" "
        delta = datetime.datetime.now() - self.start
        if msg:
            print(f"Test {test_name} {red('BAD' + msg)}, {delta}")
        elif one == two:
            print(f"Test {test_name} {green('GOOD')}, {delta}")
        else:
            print(f"Test {test_name} {red('BAD')}" + red(f"{one} != {two}") + f", {delta}")


    def before(self):
        self.start = datetime.datetime.now()

    def after(self):
        clear_log()

    def test_fib(self):
        for file, expected in [("log", ["3", "5", "8"]), ("fib", ["10946"]), ("euclidean_algorithm", ["21"]),
                               ("function_calls", ["7", "5", "10"]), ("if", ["1", "2", "4"]),
                               ("void", ["1", "3", "1", "1", "2", "3"]), ("basic", ["6", "12"]),
                               ("while", ["1", "1", "1", "2", "3"])]:
            self.before()
            run_program(file)
            self.equal(get_log(), expected, name=file)
            self.after()


if __name__ == "__main__":
    with open("build/log.txt", "w") as f:
        pass
    args = sys.argv
    if len(args) == 2:
        run_program(args[1])
        get_log()
    else:
        init()
        t = Test()
        for method in dir(t):
            if method.startswith("test"):
                getattr(t, method)()
