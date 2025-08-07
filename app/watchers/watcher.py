from abc import ABC, abstractmethod
from typing import Any


class Watcher(ABC):
    """
    Abstract base class for watchers.
    """

    @abstractmethod
    def watch(self) -> Any:
        """
        Method to be implemented by subclasses to define the watch behavior.
        """
        pass
