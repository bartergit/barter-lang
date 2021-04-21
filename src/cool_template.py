stack = []
top_pointer_stack = [0]


def dif():
    stack.append(-stack.pop() + stack.pop())


def sum():
    stack.append(stack.pop() + stack.pop())


def div():
    stack.append(1 / stack.pop() * stack.pop())


def mul():
    stack.append(stack.pop() * stack.pop())


def cout():
    print(stack.pop(), end=" ")
