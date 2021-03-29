stack = []
top_pointer_stack = [0]
true = True
false = False


def cout():
    print(",".join(reversed([str(stack.pop()) for _ in range(stack.pop())])))


def sum():
    stack.append(stack.pop() + stack.pop())

def lt():
    stack.append(stack.pop() < stack.pop())

def dif():
    stack.append(stack.pop() - stack.pop())
