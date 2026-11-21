"""Language 1: [origin] tool("argument")."""
import ply.lex as lex
import ply.yacc as yacc

from ..models import Finding, Layer, Result
from . import lexer as lexer_rules
from . import parser as parser_rules

_lexer = lex.lex(module=lexer_rules)
_parser = yacc.yacc(module=parser_rules, start="action", write_tables=False, debug=False)


def analyze_call(text: str) -> Result:
    """Return Result(tree=Call(origin, tool, argument)), or the first error found."""
    # 1. Lexer: split the line into tokens.
    _lexer.errors = []
    _lexer.inside_parens = False
    _lexer.input(text)
    tokens = list(_lexer)
    if _lexer.errors:
        return Result(None, _lexer.errors)

    # 2. Parser: check the tokens follow  ORIGIN TOOL ( QUOTED_STRING ).
    remaining = iter(tokens)
    try:
        tree = _parser.parse(lexer=_lexer, tokenfunc=lambda: next(remaining, None))
    except parser_rules.CallSyntaxError as error:
        message = parser_rules.syntax_message(tokens, error.token)
        return Result(None, [Finding(Layer.SYNTAX, message)])
    return Result(tree)
