from ..models import Finding, Layer, Result


def analyze_sql(text: str) -> Result:
    # TODO: tree = nodes.Program
    return Result(None, [Finding(Layer.SYNTAX, "SQL not implemented")])
