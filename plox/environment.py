

from tokens import Token
from typing import Mapping
import lox_interpreter

class Environment():
    values : Mapping[str, object]

    def __init__(self, enclosing = None):
        self.values = {}
        self.enclosing = enclosing
    
    def define(self, name: str, value):
        self.values[name] = value

    def get(self, name: Token):
        if name.lexeme in self.values:
            return self.values[name.lexeme]
        
        if not self.enclosing is None:
            return self.enclosing.get(name)

        raise lox_interpreter.RuntimeError(name, "Undefined variable '" + name.lexeme+".")

    def assign(self, name: Token, value):
        if name.lexeme in self.values:
            self.values[name.lexeme] = value
        elif not self.enclosing is None:
            return self.enclosing.assign(name, value)
        else:
            raise lox_interpreter.RuntimeError(name, "Undefined variable '" + name.lexeme+".")