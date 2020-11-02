from abc import ABC
from tokens import Token

class Stmt(ABC):
    def accept(self, visitor):
        return visitor.visit(self)

class Block(Stmt):
    def __init__(self, statements):
        self.statements = statements
        assert(isinstance(statements,List))
class Expression(Stmt):
    def __init__(self, expression):
        self.expression = expression
        assert(isinstance(expression,Expr))
class Print(Stmt):
    def __init__(self, expression):
        self.expression = expression
        assert(isinstance(expression,Expr))
class Var(Stmt):
    def __init__(self, name, initializer):
        self.name = name
        self.initializer = initializer
        assert(isinstance(name,Token))
        assert(isinstance(initializer,Expr))