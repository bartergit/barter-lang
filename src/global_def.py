from create_ast import *


class Global:
    variables = {}
    arrays = {}
    functions = {}
    ind = 0
    return_type = None

    @staticmethod
    def sum(x, y):
        return f"stack.append({x}); stack.append({y}); sum(); "

    @staticmethod
    def dif(x, y):
        return f"stack.append({y}); stack.append({x}); dif(); "

    @staticmethod
    def lt(x, y):
        return f"stack.append({y}); stack.append({x}); lt(); "

    @staticmethod
    def cout(*args):
        out = ""
        for arg in args:
            out += f"stack.append({arg}); "
        return out + f"stack.append({len(args)}); cout(); "

    @staticmethod
    def cond(compare, block):
        out = f"\nif {compare}: "
        out += block
        return out + "\n"

    @staticmethod
    def dec_var(name, typeof, value):
        if Global.variables.get(name) is None:
            assert typeof in types
            Global.variables[name] = dec_var(typeof, Global.ind)
            Global.ind += 1
            return f"stack.append({value}); "
        raise Exception(f"{name} is already declared")

    @staticmethod
    def set_var(name, value):
        if Global.variables.get(name) is not None:
            ind = Global.variables[name].ind
            return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
        raise Exception(f"{name}??")

    # refs

    @staticmethod
    def dec_ref(name, typeof, var_name):
        if Global.variables.get(name) is None:
            assert typeof in types
            assert var_name in Global.variables
            Global.variables[name] = dec_var('int', Global.ind)
            Global.ind += 1
            value = f"top_pointer_stack[-1] + {Global.variables[var_name].ind}"
            return f"stack.append({value}); "
        raise Exception(f"{name} is already declared")

    @staticmethod
    def deref(index):
        return f"stack.append(stack[{index}]); "

    @staticmethod
    def set_ref(index, value):
        return f"stack[{index}] = {value}"

    # end refs

    # arrays
    @staticmethod
    def dec_arr(name, typeof, size):
        if Global.variables.get(name) is None:
            assert typeof in types
            Global.variables[name] = dec_arr("arr " + typeof, Global.ind, int(size))
            Global.ind += int(size)
            return f"stack.append(0); " * int(size) # should be changed
        # if Global.arrays.get(name) is None:
        #     assert typeof in types
        #     Global.arrays[name] = dec_arr("arr " + typeof, Global.ind, int(size))
        #     Global.ind += int(size)
        #     return f"stack.append(0); " * int(size)
        raise Exception(f"{name} is already declared")

    @staticmethod
    def index(name, pos_index):
        # if Global.arrays.get(name):
        #     pos_index = int(pos_index)
        #     assert 0 <= pos_index < Global.arrays[name].size, f"{name}[{pos_index}]??"
        #     ind = Global.arrays[name].ind + pos_index
        #     return f"stack.append(stack[top_pointer_stack[-1]+{ind}]); "
        if Global.variables.get(name):
            #pos_index = int(pos_index)
            # assert 0 <= pos_index, f"{name}[{pos_index}]??"  # < Global.arrays[name].size, f"{name}[{pos_index}]??"
            ind = f"{Global.variables[name].ind} + {pos_index}"
            return f"stack.append(stack[top_pointer_stack[-1]+{ind}]); "
        raise Exception(f"{name}??")

    @staticmethod
    def set_arr(name, pos_index, value):
        if Global.variables.get(name) is not None:
            pos_index = int(pos_index)
            # assert 0 <= pos_index # < Global.v[name].size
            ind = Global.variables[name].ind + pos_index
            return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
        # if Global.arrays.get(name) is not None:
        #     pos_index = int(pos_index)
        #     assert 0 <= pos_index < Global.arrays[name].size
        #     ind = Global.arrays[name].ind + pos_index
        #     return f"stack[top_pointer_stack[-1]+{ind}] = {value}; "
        raise Exception(f"{name}??")

    # end of array
    @staticmethod
    def set_arg(name, typeof):
        assert 'arr' not in typeof, "you cant pass array by value, only as ref"
        assert typeof in types, f"'{typeof}' is not in types"
        Global.variables[name] = dec_var(typeof, Global.ind)
        Global.ind += 1
        return ""

    @staticmethod
    def dec_func(name, _return_type, _args, body_block):
        return f"\ndef {name}():\n    global stack; {body_block}\n"

    @staticmethod
    def ret_void():
        return f"stack = Stack(stack[:top_pointer_stack.pop()]); return;\n"

    @staticmethod
    def ret(value):
        return f"   stack[top_pointer_stack[-1]] = {value}; stack = Stack(stack[:top_pointer_stack.pop() + 1]); return;\n"

    corresponding = {
        "sum": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], sum),
        "dif": signature("int", [expression(value='x', type='int'), expression(value='y', type='int')], dif),
        "lt": signature("bool", [expression(value='x', type='int'), expression(value='y', type='int')], lt),
        "dec_func": signature("system", [
            expression(value='name', type='str'), expression(value='return_type', type='str'),
            expression(value='args', type='block'), expression(value='body', type='block')], dec_func),
        "set_arg": signature("system", [
            expression(value='arg_name', type='str'), expression(value='arg_type', type='str')], set_arg),
        "index": signature("system", [
            expression(value='array_name', type='str'), expression(value='index', type='int')], index),
        "dec_ref": signature("system", [
            expression(value='ref_name', type='str'), expression(value='ref_type', type='str'),
            expression(value='ref_to', type='str')], dec_ref),
        "deref": signature("int", [
            expression(value='ref', type='int')], deref)
    }
