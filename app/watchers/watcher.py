from abc import ABC, abstractmethod


class Watcher(ABC):
    """
    Abstract base class for watchers.
    """

    @abstractmethod
    def watch(self):
        """
        Method to be implemented by subclasses to define the watch behavior.
        """
        pass
