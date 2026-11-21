"""
Reads the file and mode line.
This is the interface that the main program uses to get the lines to analyze.
"""


def load(path: str) -> tuple[str, list[tuple[int, str]]]:
    """Return (mode, [(number, line), ...]). """
    mode, actions = "normal", []
    with open(path, encoding="utf-8-sig") as file:
        for line in file:
            line = line.strip()
            if line.startswith("#"):
                mode = read_mode(line) or mode
            elif line:
                actions.append((len(actions) + 1, line))
    return mode, actions


def read_mode(comment: str) -> str | None:
    """Return the mode from a comment line, or None if not found. """
    key, colon, value = comment.lstrip("#").partition(":")
    if not colon or key.strip().lower() != "modo":
        return None
    value = value.strip().lower()
    return value if value in ("normal", "congelado") else None
