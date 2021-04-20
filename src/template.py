class Stack:
    def __init__(self, array=None, n=50):
        if array is not None:
            self.array = array + [0] * (n - len(array))
            self.index = len(array)
        else:
            self.array = [0] * n
            self.index = 0

    def append(self, value):
        self.array[self.index] = value
        self.index += 1

    def pop(self):
        self.index -= 1
        value = self.array[self.index]
        return value

    def __len__(self):
        return self.index

    def __getitem__(self, index):
        if index == -1:
            return self.array[self.index - 1]
        return self.array[index]

    def __setitem__(self, key, value):
        self.array[key] = value


stack = Stack()
top_pointer_stack = Stack()
top_pointer_stack.append(0)
true = True
false = False


def ncout():
    print(" ".join(reversed([str(stack.pop()) for _ in range(stack.pop())])))


def cout():
    print(" ".join(reversed([str(stack.pop()) for _ in range(stack.pop())])), end=" ")


def sum():
    stack.append(stack.pop() + stack.pop())


def lt():
    stack.append(stack.pop() < stack.pop())


def dif():
    stack.append(stack.pop() - stack.pop())
