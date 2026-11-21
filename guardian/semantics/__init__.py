from ..models import Action, Finding
from ..url import url_rules
from . import general_rules, sql_rules


def evaluate(action: Action) -> list[Finding]:
    rules = sql_rules if action.tool == "consultar_bd" else url_rules
    return rules.evaluate(action.tree) + general_rules.evaluate(action)
