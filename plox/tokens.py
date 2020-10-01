from token_type import TokenType 

class Token(object):
    type: TokenType
    lexeme: str
    literal: object
    line: int

    def __init__(self, type, lexeme, literal, line):
        self.type = type
        self.lexeme = lexeme
        self.literal = literal
        self.line = line
    
    def __str__(self):
        return "%s %s %s" % (self.type.__str__(), self.lexeme.__str__(), self.literal.__str__())    