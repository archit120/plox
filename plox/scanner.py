from os import curdir, stat
from typing import List, Literal
from token_type import TokenType
from tokens import Token
import plox


class Scanner():
    source: str
    tokens: List[str]

    start: int
    current: int
    line: int

    keywords = {
        "and": TokenType.AND,
        "class": TokenType.CLASS,
        "else": TokenType.ELSE,
        "false": TokenType.FALSE,
        "for": TokenType.FOR,
        "fun": TokenType.FUN,
        "if": TokenType.IF,
        "nil": TokenType.NIL,
        "or": TokenType.OR,
        "print": TokenType.PRINT,
        "return": TokenType.RETURN,
        "super": TokenType.SUPER,
        "this": TokenType.THIS,
        "true": TokenType.TRUE,
        "var": TokenType.VAR,
        "while": TokenType.WHILE,
    }

    def __init__(self, source):
        self.source = source
        self.start = self.current = 0
        self.line = 1
        self.tokens = []
    

    def scan_tokens(self):
        while not self.is_eof():
            self.start = self.current
            self.scan_token()

        self.tokens.append(Token(TokenType.EOF, "", None, self.line))

        return self.tokens

    def is_eof(self):
        return self.current >= len(self.source)

    def advance(self):
        self.current += 1
        return self.source[self.current-1]


    def add_token(self, type: TokenType,  literal = None):
        text = self.source[self.start:self.current]
        self.tokens.append(Token(type, text, literal, self.line))

    def match(self, expected):
        if self.is_eof():
            return False
        if self.source[self.current] != expected:
            return False
        self.current += 1
        return True

    def peek(self):
        if self.is_eof():
            return '\0'
        return self.source[self.current]

    def handle_slash(self):
        if self.match('/'):
            while self.peek() != '\n' and not self.is_eof():
                self.advance()
        elif self.match('*'):
            openc = 1
            self.advance()
            while openc>0 and not self.is_eof():
                if self.peek() == '/' and self.peek_next() == '*':
                    openc += 1
                    self.advance()
                elif self.peek() == '*' and self.peek_next() == '/':
                    openc -= 1
                    self.advance()
                self.advance()
        else:
            self.add_token(TokenType.SLASH)
    


    def new_line(self):
        self.line += 1

    def string(self):
        while self.peek() != '"' and not self.is_eof():
            if self.peek() == '\n':
                self.line += 1
            self.advance()

        if self.is_eof():
            plox.error(self.line, "Unterminated string")
            return

        self.advance()

        val = self.source[self.start+1:self.current-1]
        self.add_token(TokenType.STRING, val)

    def peek_next(self):
        if self.current+1 >= len(self.source):
            return '\0'
        return self.source[self.current+1]

    def number(self):
        while self.peek().isdigit():
            self.advance()

        if self.peek() == '.' and self.peek_next().isdigit():
            self.advance()
            while self.peek().isdigit():
                self.advance()
        self.add_token(TokenType.NUMBER, float(
            self.source[self.start:self.current]))

    def identifier(self):
        while self.peek().isalnum() or self.peek() == '_':
            self.advance()
        text = self.source[self.start:self.current]
    
        if text in self.keywords:
            self.add_token(self.keywords[text])
        else:
            self.add_token(TokenType.IDENTIFIER)

    def scan_token(self):
        c = self.advance()

        cswitch = {
            '(': lambda x: x.add_token(TokenType.LEFT_PAREN),
            ')': lambda x: x.add_token(TokenType.RIGHT_PAREN),
            '{': lambda x: x.add_token(TokenType.LEFT_BRACE),
            '}': lambda x: x.add_token(TokenType.RIGHT_BRACE),
            ',': lambda x: x.add_token(TokenType.COMMA),
            '.': lambda x: x.add_token(TokenType.DOT),
            '-': lambda x: x.add_token(TokenType.MINUS),
            '+': lambda x: x.add_token(TokenType.PLUS),
            ';': lambda x: x.add_token(TokenType.SEMICOLON),
            '*': lambda x: x.add_token(TokenType.STAR),
            '!': lambda x: x.add_token(TokenType.BANG_EQUAL if x.match('=') else TokenType.BANG),
            '=': lambda x: x.add_token(TokenType.EQUAL_EQUAL if x.match('=') else TokenType.EQUAL),
            '<': lambda x: x.add_token(TokenType.LESS_EQUAL if x.match('=') else TokenType.LESS),
            '>': lambda x: x.add_token(TokenType.GREATER_EQUAL if x.match('=') else TokenType.GREATER),
            '/': lambda x: x.handle_slash(),
            ' ': lambda x: x,
            '\t': lambda x: x,
            '\r': lambda x: x,
            '\n': lambda x: x.new_line(),
            '"': lambda x: x.string()
        }

        if c in cswitch:
            cswitch[c](self)
            return
        elif c.isdigit():
            self.number()
            return
        elif c.isalpha() or c == '_':
            self.identifier()
            return
        else:
            plox.error(self.line, "Unexpected Character")
