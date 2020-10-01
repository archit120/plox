# plox: An implementation of the scanning tree interpreter for lox in python

wip

Challenges in 2.1
Q1) The lexical grammars of Python and Haskell are not regular. What does that mean, and why aren’t they?
Ans. Python uses indentation to find nesting. This depends on previous knowledge and is no longer a context free language.

Q. Aside from separating tokens—distinguishing print foo from printfoo—spaces aren’t used for much in most languages. However, in a couple of dark corners, a space does affect how code is parsed in CoffeeScript, Ruby, and the C preprocessor. Where and what effect does it have in each of those languages?
Ans. some preprocessor directives in C might depend on space

Q. Our scanner here, like most, discards comments and whitespace since those aren’t needed by the parser. Why might you want to write a scanner that does not discard those? What would it be useful for?
Ans. Documentation generation from code

Q. Add support to Lox’s scanner for C-style /* ... */ block comments. Make sure to handle newlines in them. Consider allowing them to nest. Is adding support for nesting more work than you expected? Why?
Ans. Done L80-L90 in scanner.py implements additional needed functionality. Nesting requires keeping track of how many additional comment blocks have been opened so its a bit more work



