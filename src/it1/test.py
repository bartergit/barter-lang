import json
import sys
import unittest
import yaml
from valid import is_dec, is_func, is_int_expr
from parse import create_func, parse
from execute import execute_function, evaluate_int_expr


class TestParser(unittest.TestCase):
    def setUp(self):
        pass
        program = """func do_nothing ( int a , int b ) int
           {
               str some = 'value2'
               bool b_2 = false
               int c = a + b
               return 5
           }
           func main ( ) void
           {
               int i = 9 - 2 * 3 * 5 + 19 / 19 - 1
               int a = 5
               int b = 9
               str str_val = 'value'
               bool flag = true
           }"""
        self.functions = {}
        self.variables = {}
        program = parse(program)
        for func in program:
            self.functions[func["name"]] = func
        execute_function(self.functions["main"], self.variables, self.functions)
        # print(self.functions)
        # print(self.variables)

    def test_create_stuff(self):
        create_func("func foo ( int a , int b ) void".split())
        create_func("func foo ( ) void".split())

    def test_is_func(self):
        self.assertTrue(is_func("func foo ( ) void".split()))
        self.assertTrue(is_func("func foo ( int a , int b ) int".split()))
        self.assertTrue(is_func("func foo_ad ( bool a_c , str bAAzz_K ) void".split()))
        self.assertFalse(is_func("func foo ad ( bool a_c , str bAAzz_K ) void".split()))
        self.assertFalse(is_func("func 1ad ( bool a_c , str bAAzz_K ) void".split()))

    def test_is_dec(self):
        self.assertTrue(is_dec("int i = 5".split()))

    def test_parse(self):
        program = """func do_nothing ( int a , int b ) void 
               {
               }
               func main ( ) void 
               {
                   int i = 5 + 1
                   str str_val = 'value'
                   bool flag = true 
               }"""
        r = parse(program)
        yaml.Dumper.ignore_aliases = lambda *args: True

    def test_is_int_expr(self):
        self.assertTrue(is_int_expr("1 + 5".split()))
        self.assertTrue(is_int_expr("1 + 5 - ( 3 + 2 ) - 9".split()))
        self.assertTrue(is_int_expr(" ( a + 1 )  ".split()))
        self.assertTrue(is_int_expr(" ( a + 1 ) + 3 ".split()))
        self.assertTrue(is_int_expr(" - ( a + 1 ) + 3 ".split()))
        self.assertTrue(is_int_expr("( - ( a + 1 ) + 3 )".split()))
        self.assertTrue(is_int_expr("( - ( a + 1 ) + 3 ) - 19 ".split()))
        self.assertTrue(is_int_expr(" + ( - ( a + 1 ) + 3 ) - 19 ".split()))
        self.assertTrue(is_int_expr("( + ( - ( a + 1 ) + 3 ) - 19 )".split()))
        self.assertTrue(is_int_expr("- 1 * ( + ( - ( a + 1 ) + 3 ) - 19 )".split()))

    def test_vars_declaration(self):
        self.assertTrue("some" not in self.variables)
        self.assertTrue("b_2" not in self.variables)
        self.assertTrue("c" not in self.variables)
        execute_function(self.functions["do_nothing"], self.variables, self.functions)
        self.assertFalse("some" not in self.variables)
        self.assertFalse("b_2" not in self.variables)
        self.assertFalse("c" not in self.variables)

    def test_eval_int_expr(self):
        self.assertEqual(evaluate_int_expr("9 - 2 * 3 * 5 + 19 / 19 - 1".split(), self.variables, self.functions), -21)
        self.assertEqual(evaluate_int_expr("( 9 - 2 ) * 2".split(), self.variables, self.functions), 14)
        self.assertEqual(evaluate_int_expr("2 * 3".split(), self.variables, self.functions), 6)
        self.assertEqual(evaluate_int_expr("2 * - 3".split(), self.variables, self.functions), -6)
        self.assertEqual(evaluate_int_expr("- 2 * - 3".split(), self.variables, self.functions), 6)
        self.assertEqual(evaluate_int_expr("- ( - 6 )".split(), self.variables, self.functions), 6)
        self.assertEqual(evaluate_int_expr("- ( - 6 ) * - 1".split(), self.variables, self.functions), -6)
        self.assertEqual(evaluate_int_expr("- ( - 6 ) + 1".split(), self.variables, self.functions), 7)
        self.assertEqual(evaluate_int_expr("- 1 * ( + ( - 6 + 3 ) - 19 )".split(), self.variables, self.functions), 22)

    def test_eval_int_expr_with_variables(self):
        self.assertEqual(evaluate_int_expr(" a + b ".split(), self.variables, self.functions), 14)
        self.assertEqual(evaluate_int_expr("b - a * a * a * 0 + 19 / 19 - 1".split(), self.variables, self.functions),
                         9)
        self.assertEqual(evaluate_int_expr("( b - a ) * 2".split(), self.variables, self.functions), 8)
        self.assertEqual(evaluate_int_expr("- ( - a )".split(), self.variables, self.functions), 5)
        self.assertEqual(evaluate_int_expr("- ( - a ) * - 1".split(), self.variables, self.functions), -5)
        self.assertEqual(evaluate_int_expr("- ( - a ) + 1".split(), self.variables, self.functions), 6)
        self.assertEqual(
            evaluate_int_expr("- 1 * ( + ( - ( a + 1 ) + 3 ) - 19 )".split(), self.variables, self.functions), 22)

    def test_is_int_expr_with_brackets(self):
        self.assertTrue(is_int_expr("1 + ( 2 - 3) - ( 1 - 19 )"))
        with self.assertRaises(Exception):
            is_int_expr("( 1 + 2 * ( 3 - 1 )")
            is_int_expr("( 1 + 2 - 3 ( ")

    def test_is_int_expr_with_func_call(self):
        self.assertTrue(is_int_expr(" 1 + foo ( 1 + 2 )".split()))
        self.assertTrue(is_int_expr(" 1 + foo ( 1 , 2 )".split()))
        self.assertFalse(is_int_expr(" 1 0 2 ".split()))
        self.assertFalse(is_int_expr(" 1 . 2 ".split()))

    def test_eval_int_expr_with_func_call(self):
        self.assertEqual(evaluate_int_expr(" 1 + do_nothing ( 1 , 2 )".split(), self.variables, self.functions), 6)
        self.assertEqual(evaluate_int_expr(" 1 + do_nothing ( 1 )".split(), self.variables, self.functions), 6)
        self.assertEqual(evaluate_int_expr(" do_nothing ( 1 )".split(), self.variables, self.functions), 5)
        self.assertEqual(evaluate_int_expr("- do_nothing ( 1 ) * do_nothing ( 2 )".split(), self.variables, self.functions), -25)

if __name__ == '__main__':
    unittest.main()