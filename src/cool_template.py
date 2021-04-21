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


if __name__ == '__main__':
    stack.append(3);
    stack.append(1);
    stack.append(2);
    mul();
    stack.append(stack.pop());
    stack.append(10);
    stack.append(1);
    div();
    print(stack)
    stack.append(stack.pop());
    dif();
    print(stack)
    stack.append(stack.pop());

    print(stack)
    sum();

    print(stack)
    stack.append(stack.pop());
    stack.append(15);
    stack.append(stack[top_pointer_stack[-1] + 0]);
    cout();
    stack.pop();