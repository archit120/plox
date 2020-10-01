import sys
import os
from sys import stderr
import scanner

hadError = False

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

    if hadError:
        exit(65)

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
        hadError = False

def run(line):
    scan = scanner.Scanner(line)
    tokens = scan.scan_tokens()

    for token in tokens:
        print(token)

def error(line, message):
    print(line, "", message)
  

def report(line, where, message):
    print("[line " + str(line) + "] Error" + where + ": " + message, file=std.stderr)
    hadError = True

if __name__ == "__main__":
    main()