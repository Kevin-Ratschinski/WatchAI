from abc import ABC, abstractmethod
from typing import Any


class Watcher(ABC):
    """Abstract base class for all watchers."""

    def __init__(self, config):
        self.config = config

    @abstractmethod
    def watch(self) -> Any:
        """Collect data from the watcher."""
        pass
