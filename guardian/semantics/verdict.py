from ..models import Action, Layer, Risk, Verdict

RISK_TO_VERDICT = {Risk.NONE: Verdict.ALLOW, Risk.MEDIUM: Verdict.CONFIRM, Risk.HIGH: Verdict.BLOCK}


def combine(action: Action) -> Verdict:
    if any(f.layer in (Layer.LEXICAL, Layer.SYNTAX) for f in action.findings):
        return Verdict.ERROR
    risk = max((f.risk for f in action.findings if f.risk is not None), default=Risk.NONE)
    return max([RISK_TO_VERDICT[risk]] + [f.verdict for f in action.findings if f.verdict is not None])
