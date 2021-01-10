from hello import parse_first, parse_sec, print_tree, evaluate_tree, parse
import unittest
class Test(unittest.TestCase):
    def test_evaluation(self):
        exprs = ["3*12+5*3-9", "3*12+5*3-9+1*15", "3*12", "3*-2", "-5", "-3*-2", "+5"]
        expected = [42, 57, 36, -6, -5, 6, 5]
        for i, expr in enumerate(exprs):
            with self.subTest(msg=f"Subtest {i}, expr: {expr}"):
                self.assertEqual(evaluate_tree(parse(expr)), expected[i])


if __name__ == '__main__':
    unittest.main()