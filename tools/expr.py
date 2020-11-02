from abc import ABC
from tokens import Token

class Expr(ABC):
    def accept(self, visitor):
        return visitor.visit(self)

class Assign(Expr):
    def __init__(self, name, value):
        self.name = name
        self.value = value
        assert(isinstance(name,Token))
        assert(isinstance(value,Expr))
class Binary(Expr):
    def __init__(self, left, operator, right):
        self.left = left
        self.operator = operator
        self.right = right
        assert(isinstance(left,Expr))
        assert(isinstance(operator,Token))
        assert(isinstance(right,Expr))
class Grouping(Expr):
    def __init__(self, expression):
        self.expression = expression
        assert(isinstance(expression,Expr))
class Literal(Expr):
    def __init__(self, value):
        self.value = value
        assert(isinstance(value,object))
class Unary(Expr):
    def __init__(self, operator, right):
        self.operator = operator
        self.right = right
        assert(isinstance(operator,Token))
        assert(isinstance(right,Expr))
class Variable(Expr):
    def __init__(self, name):
        self.name = name
        assert(isinstance(name,Token))