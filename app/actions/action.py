from abc import ABC, abstractmethod


class Action(ABC):
    """Abstract base class for all actions."""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def execute(self, data: str):
        """Execute the action with the given data."""
        pass
