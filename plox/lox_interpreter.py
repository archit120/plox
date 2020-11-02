from stmt import Expression, Print
from expr import *
from token_type import *
import plox
        

class Interpreter():
    def evaluate(self, expr):
        return expr.accept(self)

    def is_truthy(self, obj):
        if obj is None:
            return False
        if isinstance(obj, bool):
            return bool(obj)
        return True

    def is_equal(self, a, b):
        if a is None and b is None:
            return True
        if a is None:
            return False
        return a==b

    def check_number_operand(self, operator, operand, right = None):
        if right is None:
            if isinstance(operand, float):
                return True
            raise RuntimeError(operator, "Operand must be a number.")
        else:
            if isinstance(operand, float) and isinstance(right, float):
                return True
            raise RuntimeError(operator, "Operands must be a number.")


    def visit_binary_expr(self, expr : Binary):
        left = self.evaluate(expr.left)
        right = self.evaluate(expr.right)

        if expr.operator.type != TokenType.PLUS:
            self.check_number_operand(expr.operator, left, right)
        if expr.operator.type == TokenType.GREATER:
            return float(left) > float(right)
        if expr.operator.type == TokenType.GREATER_EQUAL:
            return float(left) >= float(right)
        if expr.operator.type == TokenType.LESS:
            return float(left) < float(right)
        if expr.operator.type == TokenType.LESS_EQUAL:
            return float(left) <= float(right)
        if expr.operator.type == TokenType.BANG_EQUAL:
            return not self.is_equal(float(left), float(right))
        if expr.operator.type == TokenType.EQUAL:
            return self.is_equal(float(left), float(right))
        if expr.operator.type == TokenType.MINUS:
            return float(left) - float(right)
        if expr.operator.type == TokenType.SLASH:
            return float(left) / float(right)
        if expr.operator.type == TokenType.STAR:
            return float(left) * float(right)
        
        # Handle addition
        # Can just delegate to python
        if not ((isinstance(left, str) and isinstance(right, str)) or (isinstance(left, float) and isinstance(right, float))):
            raise RuntimeError(expr.operator, "Operands must be two numbers or two strings.")
        return left + right

    def visit(self, expr):
        if isinstance(expr, Binary):
            return self.visit_binary_expr(expr)
        elif isinstance(expr, Grouping):
            return self.evaluate(expr.expression)
        elif isinstance(expr, Literal):
            return expr.value
        elif isinstance(expr, Unary):
            right = self.evaluate(expr.right)
            if expr.operator.type == TokenType.MINUS:
                self.check_number_operand(expr.operator, right)
                return -float(right)
            return not self.is_truthy(right) # Handle Bang operator
        elif isinstance(expr, Print):
            value = self.evaluate(expr.expression)
            print(self.stringify(value))
        elif isinstance(expr, Expression):
            self.evaluate(expr.expression)

    def interpret(self, statements):
        try:
            for statement in statements:
                self.execute(statement)
        except RuntimeError as e:
            plox.runtime_error(e)
        except ZeroDivisionError as e:
            plox.runtime_error(RuntimeError(Token(TokenType.SLASH, "/", None, 1), "Division by zero is not allowed"))

    def execute(self, stmt):
        stmt.accept(self)

    def stringify(self, obj):
        if obj is None:
            return "nil"
        if isinstance(obj, float):
            text = str(obj)
            if text.endswith(".0"):
                return text[:-2]
            return text
        if isinstance(obj, bool):
            return str(obj).lower()
        return str(obj)

            
class RuntimeError(Exception):
    def __init__(self, token, message):
        super().__init__(message)
        self.token = token

