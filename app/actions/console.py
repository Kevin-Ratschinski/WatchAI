from actions.action import Action

class ConsoleAction(Action):
    """An action that prints the data to the console."""

    def execute(self, data: str):
        """Prints the given data to the console."""
        print(f"Action (ConsoleAction): {data}")
