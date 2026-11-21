"""Parser of the call language."""
from .lexer import tokens  
from .nodes import Call

start = "action"


def p_action(p):
    #format
    "action : ORIGIN TOOL LPAREN QUOTED_STRING RPAREN"    
    p[0] = Call(origin=p[1][1:-1], tool=p[2], argument=p[4][1:-1])


class CallSyntaxError(Exception):
    """Raised by p_error with the token that broke the rule"""
    def __init__(self, token):
        self.token = token


def p_error(p):
    raise CallSyntaxError(p)


# What each position of the rule expects, in order.
EXPECTED = (
    "an origin like [usuario] at the start",
    "a tool name after the origin",
    "'(' after the tool name",
    "the argument in double quotes after '('",
    "')' after the argument",
)


def syntax_message(tokens: list, bad) -> str:
    """The rule is a fixed sequence, so the bad token's position says what was expected."""
    if bad is None:
        return f"expected {EXPECTED[len(tokens)]}, but the line ended"
    position = tokens.index(bad)
    if position >= len(EXPECTED):
        return f"unexpected '{bad.value}' after ')'"
    return f"expected {EXPECTED[position]}, found '{bad.value}'"