from abc import ABC, abstractmethod


class Watcher(ABC):
    """Abstract base class for all watchers."""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def watch(self) -> str:
        """Collect data from the watcher."""
        pass
