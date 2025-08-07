# WatchAI

WatchAI is a monitoring tool that uses AI to analyze data from various sources.

## Configuration

The `config.yaml` file has three main sections:

- `ollama`: Configures the Ollama analyzer.
- `watchers`: A list of watchers to collect data.
- `actions`: A list of actions to be executed.

### Watchers

Each watcher has the following properties:

- `name`: The name of the watcher (e.g., `screen_watcher`).
- `enabled`: Whether the watcher is enabled.
- `interval_seconds`: The interval in seconds at which the watcher collects data.
- `prompt`: The prompt to be used for the analysis.

### Actions

Each action has the following properties:

- `name`: The name of the action (e.g., `console_action`).
- `enabled`: Whether the action is enabled.
