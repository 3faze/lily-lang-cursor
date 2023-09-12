import sys

class LexicalToken:
    def __init__(self, token_type, token_value):
        self.token_type = token_type
        self.value = token_value

def next_token(src):
    # Current char also keeps track of the length of the current token
    current_char = 0

    # We use this to automatically handle the case where n >= len(src) everywhere
    def get_char(n):
        if n >= len(src):
            return "\0"
        else:
            return src[n]

    # Tells us if a character can be part of an identifier
    def is_ident_character(c, first):
        if first:
            return c.isalpha() or c == "_"
        else:
            # Identifiers can have numbers in them, just not as the first character
            return c.isalnum() or c == "_"

    if get_char(current_char) == "\0":
        return "EOF", current_char

    if get_char(current_char) == "(":
        current_char += 1
        return "LPAREN", current_char

    if get_char(current_char) == ")":
        current_char += 1
        return "RPAREN", current_char

    if get_char(current_char) == ",":
        current_char += 1
        return "COMMA", current_char

    if get_char(current_char) == "#":
        while get_char(current_char) != "\n" and get_char(current_char) != "\0":
            current_char += 1
        return "COMMENT", current_char

    if get_char(current_char) == "+":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "ADD_EQ", current_char
        return "ADD", current_char

    if get_char(current_char) == "-":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "SUB_EQ", current_char
        return "SUB", current_char

    if get_char(current_char) == "*":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "MUL_EQ", current_char
        return "MUL", current_char

    if get_char(current_char) == "/":
        current_char += 1
        if get_char(current_char) == "=":
            current_char += 1
            return "DIV_EQ", current_char
        return "DIV", current_char

    if get_char(current_char) == ";":
        current_char += 1
        return "SEMI", current_char

    if get_char(current_char) == '"':
        current_char += 1
        while get_char(current_char) != '"':
            current_char += 1

        return "STRING", current_char

    if get_char(current_char) == "<":
        current_char += 1
        if get_char(current_char) == "<":
            current_char += 1
            if get_char(current_char) == "=":
                current_char += 1
                return "LSHIFT_EQ", current_char
            return "LSHIFT", current_char
        if get_char(current_char) == "=":
            current_char += 1
            return "LT_EQ", current_char
        return "LT", current_char

    if get_char(current_char) == ">":
        current_char += 1
        if get_char(current_char) == ">":
            current_char += 1
            if get_char(current_char) == "=":
                current_char += 1
                return "RSHIFT_EQ", current_char
            return "RSHIFT", current_char
        if get_char(current_char) == "=":
            current_char += 1
            return "GT_EQ", current_char
        return "GT", current_char

    if get_char(current_char).isspace():
        while get_char(current_char).isspace():
            current_char += 1
        return "WHITESPACE", current_char

    if get_char(current_char).isdigit():
        while get_char(current_char).isdigit():
            current_char += 1
        return "NUMBER", current_char

    if is_ident_character(get_char(current_char), True):
        while is_ident_character(get_char(current_char), False):
            current_char += 1

        if src[:current_char] == "if":
            return "KW_IF", current_char
        if src[:current_char] == "else":
            return "KW_ELSE", current_char
        if src[:current_char] == "return":
            return "KW_RETURN", current_char

        return "IDENT", current_char
