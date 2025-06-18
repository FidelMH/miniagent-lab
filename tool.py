from __future__ import annotations

class Tool:
    """Base class for external tools."""
    name: str

    def __init__(self, name: str):
        self.name = name

    def run(self, args: str) -> str:
        """Override this method to implement tool logic."""
        raise NotImplementedError("Tool.run must be implemented by subclasses")
