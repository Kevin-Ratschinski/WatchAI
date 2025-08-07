from actions.action import Action


class ConsoleAction(Action):
    """An action that prints the data to the console."""

    def __init__(self, config):
        super().__init__(config)

    def execute(self, data: str):
        """Prints the given data to the console."""
        print(f"Action (ConsoleAction): {data}")
