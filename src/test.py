from parse_expr import parse_first, parse_sec, print_tree, evaluate_tree, parse
from help import print_as_yaml, load_from_yaml, save_as_yaml
from parse_program import create_program, create_func_call
from execute import execute
import unittest


class Test(unittest.TestCase):
    def setUp(self) -> None:
        self.variables = {}
        self.functions = load_from_yaml("out/built_in.yaml")

    def test_evaluation(self):
        pass
        # exprs = ["3*12+5*3-9", "3*12+5*3-9+1*15", "3*12", "3*-2", "-5", "-3*-2", "+5"]
        # expected = [42, 57, 36, -6, -5, 6, 5]
        # for i, expr in enumerate(exprs):
        #     with self.subTest(msg=f"Subtest {i}, expr: {expr}"):
        #         self.assertEqual(evaluate_tree(parse(expr)), expected[i])

    def test_execution(self):
        with open("out/main.bl") as main:
            with open("out/log.txt", "w+") as log:
                log.write("")
            functions = create_program(main.read(), self.variables, self.functions)
            save_as_yaml(functions, "out/main.yaml")
            program = load_from_yaml("out/main.yaml")
            variables = execute(program)
            self.assertEqual(variables["six"]["value"], 6)
            self.assertEqual(variables["three"]["value"], 3)
            self.assertEqual(variables["eight"]["value"], 8)
            self.assertEqual(variables["five"]["value"], 5)
            self.assertEqual(variables["a"]["value"], 19)
            with open("out/log.txt", "r") as log:
                self.assertEqual(log.read().split("\n")[:-1], ["something", "1", "17", "hello world"])

    def test_create_func_call(self):
        tests = [
            "nothing()",
            "log('hello world')",
            "add(19, 1)",
            "log(to_str(div(15, 10)))",
            "log(to_str(sub(19, mult(2, div(15, 10)))))",
            "and(not(and(true,true)),not(or(true,false)))"]
        for test in tests:
            with self.subTest(i=test):
                create_func_call(test, self.variables, self.functions)

    def test_recursion(self):
        with open("out/recursion.bl") as main:
            with open("out/log.txt", "w+") as log:
                log.write("")
            functions = create_program(main.read(), self.variables, self.functions)
            save_as_yaml(functions, "out/recursion.yaml")
            program = load_from_yaml("out/recursion.yaml")
            execute(program)
            with open("out/log.txt", "r") as log:
                self.assertEqual(log.read().split("\n")[:-1], ["120", "144"])

    def test_fail_for_now(self):
        pass


if __name__ == '__main__':
    # fib = lambda x: x if x == 0 or x == 1 else fib(x - 1) + fib(x - 2)
    # print(fib(30))
    unittest.main()
