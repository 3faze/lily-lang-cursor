from lexer import *
from astgen import *
import sys

filename = sys.argv[1]
src = open(filename, "r").read()
token_iter = tokenize(src)
token_stream = TokenStream(token_iter, src)
expression = parse_expression(token_stream)
print(expression)
