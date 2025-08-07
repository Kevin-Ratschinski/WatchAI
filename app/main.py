import time

import yaml
from analyzers.ollama import OllamaAnalyzer
from watchers.screen import ScreenWatcher


def load_config(config_path="config.yaml"):
    """Load the configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        print(f"Error: Configuration file '{config_path}' not found.")
        exit(1)
    except yaml.YAMLError as e:
        print(f"Error parsing YAML configuration: {e}")
        exit(1)


def main():
    config = load_config()

    # Initialize watchers based on the configuration
    watchers = {}
    for watcher_config in config.get('watchers', []):
        if watcher_config.get('enabled'):
            watcher_name = watcher_config['name']
            if watcher_name == 'screen_watcher':
                watchers[watcher_name] = {
                    'instance': ScreenWatcher(watcher_config),
                    'interval': watcher_config.get('interval', 10),
                    'prompt': watcher_config.get('prompt', '')
                }
                print(
                    f"'{watcher_name}' initialized with interval: {watchers[watcher_name]['interval']}s")
            else:
                print(f"Unknown watcher type: {watcher_name}. Ignored.")

    if not watchers:
        print("No active watchers found in the configuration. Exiting.")
        return

    ollama_analyzer = OllamaAnalyzer(config)

    print("\nStarting monitoring loop. Press Ctrl+C to exit.")
    try:
        while True:
            for watcher_name, watcher_info in watchers.items():
                print(f"\n--- Starting cycle for {watcher_name} ---")
                watcher_instance = watcher_info['instance']
                interval = watcher_info['interval']
                prompt = watcher_info['prompt']

                # Data collection
                collected_data = watcher_instance.watch()

                if collected_data:
                    # Analysis
                    llm_response = ollama_analyzer.analyze(
                        collected_data, prompt)
                    print(f"LLM Response: {llm_response}")

                    # Action module (ConsoleAction prototype)
                    print(f"Action (ConsoleAction): {llm_response}")
                else:
                    print(
                        f"No data collected from {watcher_name}. Skipping analysis.")

                print(
                    f"Waiting {interval} seconds until next cycle for {watcher_name}...")
                time.sleep(interval)  # Wait after each watcher cycle

    except KeyboardInterrupt:
        print("\nMonitoring stopped.")


if __name__ == "__main__":
    main()
