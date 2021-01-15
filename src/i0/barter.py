import unittest

types = ["str", "bool", "int"]
operations = ["+", "-"]
special = ["true", "false"]

def is_name(text):
    return text not in types and text not in special and text[0].isalpha()

def is_int(text):
    return text.isnumeric()

def is_str(text):
    return text[0] == "'" and text[-1] == "'"

def is_bool(text):
    return text == "true" or text == "false"


def is_int_expr(tokens):
    return False not in map(lambda x: is_int(x) or is_name(x) or x in operations, tokens)

def is_str_expr(tokens):
    return len(tokens) == 1 and is_str(tokens[0])

def is_bool_expr(tokens):
    return len(tokens) == 1 and is_bool(tokens[0])


def is_decl(tokens):
    if len(tokens) <= 3 or tokens[0] not in types:
        return False
    if tokens[0] == "int":
        return is_name(tokens[1]) and tokens[2] == "=" and is_int_expr(tokens[3:])
    if tokens[0] == "str":
        return is_name(tokens[1]) and tokens[2] == "=" and is_str_expr(tokens[3:])
    if tokens[0] == "bool":
        return is_name(tokens[1]) and tokens[2] == "=" and is_bool_expr(tokens[3:])


def clear_line(line):
    tokens = []
    for ind, line_part in enumerate(line.split("'")):
        if ind % 2 == 0:
            tokens += line_part.split()
        else:
            tokens += ["'" + line_part + "'"]
    return tokens[:tokens.index("//")] if "//" in tokens else tokens

def is_valid_line(line):
    tokens = clear_line(line)
    return is_decl(tokens) or line.strip() == ""

def is_valid_program(program_text):
    return False not in map(is_valid_line, program_text.split("\n"))


class TestParser(unittest.TestCase):
    def test_is_valid_decl(self):
        program = """
        int i = 5 + 9 // comment1
        str str_value = 'someth  ing' // comment2
        bool flag_value = true // comment3
        bool flag_value = false // comment4
        """.split("\n")
        for line in program:
            with self.subTest(i=line):
                self.assertTrue(is_valid_program(line))

    def test_not_valid_decl(self):
        program = """int i = 'some'
        int i = true
        int i = 
        int i = //35
        str str_value = 'str0' + 'str1'
        str str_value = 35
        str str_value = true
        bool flag_value = 35
        bool flag_value = false + true
        bool flag_value = 35 + 9""".split("\n")
        for line in program:
            with self.subTest(i=line):
                self.assertFalse(is_valid_program(line))

    def test_should_fail(self):
        program = """
        func do(){
            print(a)
        }
        func main(){
            int i = 5 + 1
            str str_val= 'value'
            bool flag = true 
            if flag {
                do()
            }
        }
        """
        self.assertFalse(is_valid_program(program))

if __name__ == '__main__':
    unittest.main()