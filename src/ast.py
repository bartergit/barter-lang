from anytree import Node, RenderTree
from collections import namedtuple
variable = namedtuple('variable', 'name')
compare = namedtuple('compare', 'operator')
bin_op = namedtuple('bin_op', 'operator')
constant = namedtuple('constant', 'value')

assign = namedtuple('assign', 'name')
# while b != 0 {
#     if a > b {
#         int a = a − b
#     } else {
#         int b = b − a
#     }
# }
# return a
program = Node("program")
whil = Node("while", parent=program)
ret = Node("ret", parent=program)
cond = Node("cond", parent=whil)
body = Node("body", parent=whil)
ret_a = Node(variable('a'), parent=ret)
comp = Node(compare("!="), parent=cond)
v1 = Node(variable("b"), parent=comp)
v2 = Node(constant(0), parent=comp)
branch = Node("branch", parent=body)
branch_condition = Node("condition", parent=branch)
if_body = Node("if_body", parent=branch)
else_body = Node("else_body", parent=branch)
op = Node(compare(">"), parent=branch_condition)
c1 = Node(variable("a"), parent=op)
c2 = Node(variable("b"), parent=op)
ass = Node(assign("a"), parent=if_body)
bin1 = Node(bin_op("-"), parent=ass)
v3 = Node(variable("a"), parent=bin1)
v4 = Node(variable("b"), parent=bin1)
ass = Node(assign("b"), parent=else_body)
bin2 = Node(bin_op("-"), parent=ass)
v3 = Node(variable("b"), parent=bin2)
v4 = Node(variable("a"), parent=bin2)
for pre, fill, node in RenderTree(program):
    print("%s%s" % (pre, node.name))



