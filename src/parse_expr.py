import operator
from help import find, minimal_but_not_negative

class Tree:
    def __init__(self, val, left=None, right=None):
        self.left = left
        self.right = right
        self.val = val

    def add_left(self, left):
        self.left = left
        left.parent = self


def print_tree(t, i=0):
    if t is not None:
        print(" " * i, t.val, sep="")
        print_tree(t.left, i + 1)
        print_tree(t.right, i + 1)

def parse_sec(t, parent=None, dir=None):
    if t.left is None and t.right is None:
        if dir == "left":
            parent.left = parse_first(t.val, "*", "/")
        elif dir == "right":
            parent.right = parse_first(t.val, "*", "/")
        else:
            return parse_first(t.val, "*", "/")
    else:
        parse_sec(t.left, t, "left")
        parse_sec(t.right, t, "right")


def parse_first(expr, s1, s2):
    ind = 0
    ind = minimal_but_not_negative(find(expr, s1, ind), find(expr, s2, ind))
    if ind == -1:
        return Tree(expr)
    tree = Tree(expr[ind], expr[:ind], expr[ind + 1:])
    tree.left = parse_first(tree.left, s1, s2)
    tree.right = parse_first(tree.right, s1, s2)
    return tree


operations = {"*": operator.mul, "/": operator.truediv, "+": operator.add, "-": operator.sub}


def evaluate_tree(tree):
    if tree.left and tree.right:
        return operations[tree.val](evaluate_tree(tree.left), evaluate_tree(tree.right))
    else:
        if tree.val == '':
            return 0
        else:
            return float(tree.val)


def parse(expr):
    expr = expr.replace("-", "+-").replace("*+", "*").replace("/+", "/")
    tree = parse_first(expr, "+", "+")
    tree = parse_sec(tree) or tree
    return tree


if __name__ == '__main__':
    expr = "-5"
    tree = parse(expr)
    print_tree(tree)
    print(evaluate_tree(tree))
