"""Lexer of the call language: [origin] tool("argument")."""
from ..models import Finding, Layer

ORIGINS = ("usuario", "documento", "mensaje")
TOOLS = ("consultar_bd", "abrir_enlace")

tokens = ("ORIGIN", "TOOL", "LPAREN", "QUOTED_STRING", "RPAREN")

t_ignore = " \t"


def t_ORIGIN(t):
    r"\[\w*\]"
    if t.value[1:-1] not in ORIGINS:
        return error(t, f"unknown origin '{t.value}'")
    return t


def t_QUOTED_STRING(t):
    r'"[^"]*"'
    return t


def t_LPAREN(t):
    r"\("
    t.lexer.inside_parens = True
    return t


def t_RPAREN(t):
    r"\)"
    t.lexer.inside_parens = False
    return t


def t_TOOL(t):
    r"[A-Za-z_]\w*"
    if t.lexer.inside_parens:
        return error(t, "expected the argument in double quotes")
    if t.value not in TOOLS:
        return error(t, f"unknown tool '{t.value}'")
    return t


def t_error(t):
    char = t.value[0]
    if char == '"':
        error(t, 'the argument is never closed (missing ")')
    elif char == "[":
        error(t, "the origin is never closed (missing ])")
    elif t.lexer.inside_parens:
        error(t, "expected the argument in double quotes")
    else:
        error(t, f"invalid character '{char}'")


def error(t, message: str) -> None:
    """Record a lexical error."""
    t.lexer.errors.append(Finding(Layer.LEXICAL, message))
    t.lexer.skip(len(t.lexer.lexdata))
