from abc import ABC
from token import Token

class Expr(ABC):
    def accept(self, visitor):
        visitor.visit(self)

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