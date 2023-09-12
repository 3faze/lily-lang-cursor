from lexer import *

# Returns a token type, it's length and it's starting location
def tokenize(src):
    to_skip = ["COMMENT", "WHITESPACE"]
    current_loc = 0

    # A convenient loop to skip tokens we don't want to parse
    while True:
        token_ty, token_len = next_token(src)
        token_start = current_loc
        current_loc += token_len

        src = src[token_len:]

        if token_ty not in to_skip:
            yield token_ty, token_start, token_len

class TokenStream:
    def __init__(self, token_iter, src):
        self.generated = []
        self.token_iter = token_iter
        self.src = src

    # Gets the nth token from the current
    def nth(self, n):
        while n >= len(self.generated):
            self.generated.append(next(self.token_iter))
        return self.generated[n]

    # Advances the token stream by one token and returns the one that was the current
    def bump(self):
        current = self.nth(0)
        self.generated = self.generated[1:]

    # Returns true if the current token matches the type
    def check(self, ty):
        return self.nth(0)[0] == ty

    def bump_if(self, ty):
        if self.check(ty):
            self.bump()
            return True
        return False

    def expect(self, ty):
        if not self.bump_if(ty):
            self.raise_unexepected()

    def token_contents(self):
        _, token_start, token_len = self.nth(0)
        return self.src[token_start:(token_start + token_len)]

    def raise_unexepected(self):
        raise Exception("Unexpected token encountered")

def parse_comma_list(token_stream, terminator):
    l = []

    # Handle the case of the empty list
    if token_stream.bump_if(terminator):
        return l

    while True:
        l.append(parse_expression(token_stream))

        if token_stream.bump_if("COMMA"):
            continue

        token_stream.expect(terminator)
        return l

def parse_base(token_stream):
    if token_stream.bump_if("LPAREN"):
        inside = parse_expression(token_stream)
        token_stream.expect("RPAREN")
        return inside

    if token_stream.check("NUMBER"):
        contents = token_stream.token_contents()
        token_stream.bump()
        return "EXPR_NUM", float(contents)

    if token_stream.check("IDENT"):
        contents = token_stream.token_contents()
        token_stream.bump()
        return "EXPR_IDENT", contents

    if token_stream.check("EOF"):
        contents = token_stream.token_contents()
        token_stream.bump()
        return "EOF", contents

    token_stream.raise_unexepected()

def parse_call(token_stream):
    lhs = parse_base(token_stream)
    while token_stream.bump_if("LPAREN"):
        args_list = parse_comma_list(token_stream, "RPAREN")
        lhs = "EXPR_CALL", lhs, args_list

    return lhs

def parse_product(token_stream):
    lhs = parse_call(token_stream)
    while True:
        if token_stream.bump_if("MUL"):
            rhs = parse_product(token_stream)
            lhs = "EXPR_MUL", lhs, rhs
            continue
        if token_stream.bump_if("DIV"):
            rhs = parse_product(token_stream)
            lhs = "EXPR_DIV", lhs, rhs
            continue
        break

    return lhs

def parse_sum(token_stream):
    lhs = parse_product(token_stream)
    while True:
        if token_stream.bump_if("ADD"):
            rhs = parse_sum(token_stream)
            lhs = "EXPR_ADD", lhs, rhs
            continue
        if token_stream.bump_if("SUB"):
            rhs = parse_sum(token_stream)
            lhs = "EXPR_SUB", lhs, rhs
            continue
        break

    return lhs

def parse_expression(token_stream):
    return parse_sum(token_stream)

def evaluate_expression(expression):
    if expression[0] == "EXPR_ADD":
        return evaluate_expression(expression[1]) + evaluate_expression(expression[2])
    if expression[0] == "EXPR_SUB":
        return evaluate_expression(expression[1]) - evaluate_expression(expression[2])
    if expression[0] == "EXPR_MUL":
        return evaluate_expression(expression[1]) * evaluate_expression(expression[2])
    if expression[0] == "EXPR_DIV":
        return evaluate_expression(expression[1]) / evaluate_expression(expression[2])
    if expression[0] == "EXPR_NUM":
        return expression[1]
    # This is just for the demo, in an actual language this would look up from a table of defined functions
    if expression[0] == "EXPR_CALL":
        to_call = expression[1]
        args = list(map(evaluate_expression, expression[2]))

        if to_call == ("EXPR_IDENT", "sqrt"):
            if len(args) != 1:
                raise Exception("Argument list invalid")
            return args[0] ** 0.5

        if to_call == ("EXPR_IDENT", "pow"):
            if len(args) != 2:
                raise Exception("Argument list invalid")
            return args[0] ** args[1]

        raise Exception("Expression not callable")

    raise Exception("Expression not evaluable")
#print(evaluate_expression(expression))
