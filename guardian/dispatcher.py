"""
Dispatcher is the core.
It is responsible for analyzing each action
and returning the results.

So the flow is:
1. Analyze the call (lexical and syntax)
2. If the call is ok, send the argument to the SQL or URL analyzer (lexical and syntax)
3. If the argument is ok, apply the rules (semantic)
4. Combine all the findings into one verdict
5. Return the action with the findings and the verdict

It never raises: any error becomes a Finding, so one broken line
doesn't stop the analysis of the others.
"""
from . import semantics
from .call import analyze_call
from .call.nodes import Call
from .models import Action, Finding, Layer
from .semantics.verdict import combine
from .sql import analyze_sql
from .url import analyze_url

ANALYZERS = {"consultar_bd": analyze_sql, "abrir_enlace": analyze_url}


def analyze_action(line: int, text: str, mode: str) -> Action:
    action = Action(line, text, mode)
    try:
        analyze(action)
    except Exception as error:  # a bug in one module only affects this line
        action.findings.append(Finding(Layer.SYNTAX, f"internal error: {error}"))
    action.verdict = combine(action)
    return action


def analyze(action: Action) -> None:
    call = analyze_call(action.text)
    action.findings += call.findings
    if not call.ok:
        return

    tree = call.tree
    assert isinstance(tree, Call)
    action.origin, action.tool, action.argument = tree.origin, tree.tool, tree.argument

    analyzer = ANALYZERS.get(tree.tool)
    if analyzer is None:
        action.findings.append(Finding(Layer.LEXICAL, f"unknown tool '{tree.tool}'"))
        return

    result = analyzer(tree.argument)
    action.tree = result.tree
    action.findings += result.findings
    if result.ok:
        action.findings += semantics.evaluate(action)
