from ..models import Finding, Layer, Result


def analyze_url(text: str) -> Result:
    # TODO: tree = nodes.Url
    return Result(None, [Finding(Layer.SYNTAX, "URL not implemented")])
