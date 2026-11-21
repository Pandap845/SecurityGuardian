from dataclasses import dataclass

@dataclass
class Call:
    origin: str
    tool: str
    argument: str
