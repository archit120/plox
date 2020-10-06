from sys import implementation
from token_type import *
from typing import List, Type
from tokens import Token
from expr import Binary, Expr, Grouping, Unary, Literal
import plox

class Parser():
    tokens: List[Token]
    current: int

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0
    
    def parse(self):
        try:
            return self.expression()
        except ParseError as e:
            return None

    def match(self, *types):
        for type in types:
            if self.check(type):
                self.advance()
                return True
        return False
    
    def check(self, type):
        if self.isAtEnd():
            return False
        return self.peek().type == type
    
    def advance(self):
        if self.isAtEnd():
            return self.previous()
        self.current+=1
    
    def isAtEnd(self):
        return self.peek().type == TokenType.EOF
    
    def peek(self):
        return self.tokens[self.current]
    
    def previous(self):
        return self.tokens[self.current-1]

    def expression(self):
        return self.equality()
    
    def equality(self):
        expr = self.comparison()

        while self.match(TokenType.BANG_EQUAL, TokenType.EQUAL_EQUAL):
            operator = self.previous()
            right = self.comparison()
            expr = Binary(expr, operator, right)

        return expr

    def comparison(self):
        expr = self.term()

        while self.match(TokenType.GREATER, TokenType.GREATER_EQUAL, TokenType.LESS, TokenType.LESS_EQUAL):
            operator = self.previous()
            right = self.term()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def term(self):
        expr = self.factor()

        while self.match(TokenType.MINUS, TokenType.PLUS):
            operator = self.previous()
            right = self.factor()
            expr = Binary(expr, operator, right)
        
        return expr
    
    def factor(self):
        expr = self.unary()

        while self.match(TokenType.SLASH, TokenType.STAR):
            operator = self.previous()
            right = self.unary()
            expr = Binary(expr, operator, right)
        
        return expr

    def unary(self):
        if self.match(TokenType.BANG, TokenType.MINUS):
            operator = self.previous()
            right = self.unary()
            expr = Unary(operator, right)
            return expr
        
        return self.primary()
    
    def primary(self):
        if self.match(TokenType.FALSE):
            return Literal(False)
        elif self.match(TokenType.TRUE):
            return Literal(True)
        elif self.match(TokenType.NIL):
            return Literal(None)
        elif self.match(TokenType.NUMBER, TokenType.STRING):
            return Literal(self.previous().literal)
        elif self.match(TokenType.LEFT_PAREN):
            expr = self.expression()
            self.consume(TokenType.RIGHT_PAREN, "Expected ')' after expression.")
            return Grouping(expr)
        
        raise self.error(self.peek(), "Expected a primary literal or a grouping.")


    def consume(self, type, message):
        if self.check(type):
            return self.advance()

        raise self.error(self.peek(), message)
    
    def error(self, token, message):
        plox.error(token, message)

        return ParseError()

    def synchronize(self):
        self.advance()

        while not self.isAtEnd():
            if self.previous().type == TokenType.SEMICOLON:
                return
            
            valid = [
                TokenType.CLASS,
                TokenType.FUN,
                TokenType.VAR,
                TokenType.FOR,
                TokenType.IF,
                TokenType.WHILE,
                TokenType.PRINT,
                TokenType.RETURN
            ]

            if self.peek().type in valid:
                return

            self.advance()
    

class ParseError(Exception):
    pass