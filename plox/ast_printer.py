from expr import *
from token_type import *

        

class ast_printer():
    def print(self, expr):
        expr.accept(self)
    
    def paranthesize(self, name, *args):
        builder = '(%s'%name
        for expr in args:
            builder = builder + ' ' + expr.accept(self)
        
        return builder+')'

    def visit(self, expr):
        if isinstance(expr, Binary):
            return self.paranthesize(expr.operator.lexeme, expr.left, expr.right)
        elif isinstance(expr, Grouping):
            return self.paranthesize('group', expr.expression)
        elif isinstance(expr, Literal):
            if expr.value is None:
                return 'nil'
            return str(expr.value)
        else:
            return self.paranthesize(expr.operator.lexeme, expr.right)


            

if __name__ == "__main__":
    expression = Binary(
        Unary(
            Token(TokenType.MINUS, "-", None, 1),
            Literal(123)
        ),
        Token(TokenType.STAR, "*", None, 1),
        Grouping(
            Literal(45.67)
        )
    )

    print(expression.accept(ast_printer()))

