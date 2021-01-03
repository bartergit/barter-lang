from util import find, rfind
from valid import is_name
from CONST import first_priority_operations, sec_priority_operations
from collections import deque
import unittest

def evaluate_int_expr(tokens, variables):
    deq = deque(tokens)
    i1, i2 = find(tokens, "("), rfind(tokens, ")")
    if i1 == -1 and i2 == -1:
        if deq[0] == "-" or deq[0] == "+":
            deq[0] = deq[0] + "1"
            deq.insert(1, "*")
        for priority_operations in [first_priority_operations, sec_priority_operations]:
            ind = 0
            temp = 0
            while ind < len(deq):
                el = deq[ind]
                if el in priority_operations:
                    if deq[ind + 1] in sec_priority_operations:
                        if is_name(deq[ind + 2]):
                            next_el = int(deq[ind + 1] + str(variables[deq[ind + 2]]["expr"]))
                        else:
                            next_el = int(deq[ind + 1] + deq[ind + 2])
                        del deq[ind]
                    else:
                        if is_name(deq[ind + 1]):
                            next_el = variables[deq[ind + 1]]["expr"]
                        else:
                            next_el = int(deq[ind + 1])
                    if el == "*":
                        temp = temp * next_el
                    elif el == "/":
                        temp = temp / next_el
                    elif el == "+":
                        temp = temp + next_el
                    elif el == "-":
                        temp = temp - next_el
                    del deq[ind]
                    del deq[ind]
                    ind -= 1
                    deq[ind] = temp
                try:
                    temp = variables[deq[ind]]["expr"] if is_name(deq[ind]) else int(deq[ind])
                except:
                    temp = deq[ind]
                ind += 1
        assert len(deq) == 1, len(deq)
        return int(deq[0])
    elif i1 != -1 and i2 != -1:
        expr = evaluate_int_expr(tokens[i1 + 1:i2], variables)
        for i in range(i2 - i1):
            del deq[i1]
        deq[i1] = expr
        return evaluate_int_expr(deq, variables)


def execute_function(func, variables):
    for body_part in func["body"]:
        if body_part["type"] == "int":
            body_part["expr"] = evaluate_int_expr(body_part["expr"], variables)
        variables[body_part["name"]] = body_part