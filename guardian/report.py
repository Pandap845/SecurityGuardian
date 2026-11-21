""" 
Prints a report of the analysis results for a
list of actions.
"""

from .models import Action, Verdict

SYMBOLS = {Verdict.ALLOW: "✔", Verdict.CONFIRM: "⚠", Verdict.BLOCK: "✖", Verdict.ERROR: "✖"}


def print_report(file_name: str, mode: str, actions: list[Action]) -> None:
    print(f"Analyzing: {file_name} (mode: {mode})")
    for a in actions:
        print(f"[{a.line}] {SYMBOLS[a.verdict]} {a.verdict.name:<8} {a.argument or a.text}")
        for f in a.findings:
            print(f"      {f.rule or f.layer.value}: {f.message}")
