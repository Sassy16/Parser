from abc import ABC, abstractmethod
import re
import math
from numpy import double


class Expression(ABC):
    @abstractmethod
    def calc(self) -> double:
        pass

# implement the classes here


class Num(Expression):
    def __init__(self, x) -> None:
        self.x = x

    def calc(self) -> double:
        return self.x


class BinExp(Expression):
    def calc(self) -> double:
        pass

    def __init__(self, left, right):
        self.left = left
        self.right = right


class Plus(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        return self.left.calc() + self.right.calc()


class Minus(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        return self.left.calc() - self.right.calc()


class Mul(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> Num:
        return (self.left.calc() * self.right.calc())


class Div(BinExp):
    def __init__(self, left, right):
        super().__init__(left, right)
        self.left = left
        self.right = right

    def calc(self) -> double:
        return self.left.calc() / self.right.calc()

# function that returns true if the parameter given can ce converted to int and returns false otherwise.
def isNum(x) -> bool:
    try:
        int(x)
        return True
    except ValueError:
        return False

# implement the parser function here
def parser(expression) -> float:

    queue = []
    stack = []
    stack_expressions = []
    afterSplitArr = re.findall("[+/*()-]|[\d.]+", expression) 
    spliters = []
    i = 0
    while i < (len(afterSplitArr) - 1):
        if afterSplitArr[i] == '-' and isNum(afterSplitArr[i + 1]):
            spliters.append(afterSplitArr[i] + afterSplitArr[i + 1])
            spliters.append('+')
            i += 2
        if afterSplitArr[i] == '-' and afterSplitArr[i + 1] == '(' and afterSplitArr[i + 2] == '-':
            spliters.append('+')
            spliters.append(afterSplitArr[i + 3])
            i += 5
        if afterSplitArr[i] == "(" and afterSplitArr[i+1] == "-":
            spliters.append(afterSplitArr[i+1] + afterSplitArr[i+2])
            i += 4
        else:
            spliters.append(afterSplitArr[i])
            i += 1
    spliters.append(afterSplitArr[len(afterSplitArr)-1])

    for s in spliters:
        if isNum(s):
            queue.append(s)
        else:
            if s in "*/":
                stack.append(s)
            elif s in "+-":
                while (len(stack) > 0) and (stack[-1] == "*" or stack[-1] == "/"):
                    queue.append(stack.pop())
                stack.append(s)
            elif s == "(":
                stack.append(s)
            elif s == ")":
                while (len(stack) > 0) and (not stack[len(stack)-1] == "("):
                    queue.append(stack.pop())
                if len(stack) > 0 and stack[len(stack)-1] == "(":
                    stack.pop()
    while len(stack) > 0:
        queue.append(stack.pop())

    for i in queue:
        if isNum(i):
            stack_expressions.append(Num(int(i)))
        else:
            right = stack_expressions.pop()
            left = stack_expressions.pop()
            if i == "+":
                stack_expressions.append(Plus(left, right))
            elif i == "-":
                stack_expressions.append(Minus(left, right))
            elif i == "*":
                stack_expressions.append(Mul(left, right))
            elif i == "/":
                stack_expressions.append(Div(left, right))

    result = math.floor(double(stack_expressions.pop().calc()))
    return result
   
