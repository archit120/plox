import sys
import os
from sys import stderr
from token_type import TokenType
from tokens import Token
import scanner
import lox_parser
import ast_printer
import lox_interpreter
import config

interpreter = lox_interpreter.Interpreter()
def main():
    if len(sys.argv) > 2:
        print("Usage: plox [script]")
        exit(64)
    elif len(sys.argv) == 2:
        run_file(sys.argv[1])
    else:
        run_prompt()

def run_file(path):
    src = None
    with open(path, "r", encoding="utf-8") as f:
        src = f.read()
    run(src)

    if config.hadError:
        exit(65)
    if config.hadRuntimeError:
        exit(70)

def run_prompt():
    while True:
        print("> ", end = "")
        sys.stdout.flush()
        line = sys.stdin.readline()
        sys.stdout.flush()
        if line!='':
            run(line)
        else:
            break
        config.hadError = False

def run(line):
    scan = scanner.Scanner(line)
    tokens = scan.scan_tokens()
    parser = lox_parser.Parser(tokens)
    statements = parser.parse()

    if config.hadError:
        return
        
    interpreter.interpret(statements)

def error(token, message):
    if isinstance(token, Token):
        if token.type == TokenType.EOF:
            report(token.line, " at end", message)
        else:
            report(token.line, " at " + token.lexeme +"'", message)
    else:
        # token = line = int
        report(token, " at end", message)

def runtime_error(error: lox_interpreter.RuntimeError):
    print(error.args[0] + "\n[line " + str(error.token.line) +"]")
    config.hadRuntimeError=True

def report(line, where, message):
    print("[line " + str(line) + "] Error" + where + ": " + message, file=sys.stderr)
    config.hadError = True

if __name__ == "__main__":
    config.init()
    main()