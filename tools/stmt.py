from abc import ABC
from tokens import Token

class Expr(ABC):
    def accept(self, visitor):
        return visitor.visit(self)

class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression
        assert(isinstance(expression,Expr))
class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
        assert(isinstance(expression,Expr))