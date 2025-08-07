import time
import yaml
import logging

from analyzers.ollama import OllamaAnalyzer
from watchers.screen import ScreenWatcher
from actions.console import ConsoleAction

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def get_action_instance(action_name):
    if action_name == 'console_action':
        return ConsoleAction()
    return None


def load_config(config_path="config.yaml"):
    """Load the configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_path}' not found.")
        exit(1)
    except yaml.YAMLError as e:
        logging.error(f"Error parsing YAML configuration: {e}")
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
                logging.info(
                    f"'{watcher_name}' initialized with interval: {watchers[watcher_name]['interval']}s")
            else:
                logging.warning(f"Unknown watcher type: {watcher_name}. Ignored.")

    if not watchers:
        logging.info("No active watchers found in the configuration. Exiting.")
        return

    # Initialize actions based on the configuration
    actions = []
    for action_config in config.get('actions', []):
        if action_config.get('enabled'):
            action_name = action_config.get('name')
            action_instance = get_action_instance(action_name)
            if action_instance:
                actions.append(action_instance)
                logging.info(f"'{action_name}' initialized.")
            else:
                logging.warning(f"Unknown action type: {action_name}. Ignored.")

    if not actions:
        logging.info("No active actions found in the configuration. Exiting.")
        return

    ollama_analyzer = OllamaAnalyzer(config)

    logging.info("Starting monitoring loop. Press Ctrl+C to exit.")
    try:
        while True:
            for watcher_name, watcher_info in watchers.items():
                try:
                    logging.info(f"--- Starting cycle for {watcher_name} ---")
                    watcher_instance = watcher_info['instance']
                    interval = watcher_info['interval']
                    prompt = watcher_info['prompt']

                    # Data collection
                    collected_data = watcher_instance.watch()

                    if collected_data:
                        # Analysis
                        llm_response = ollama_analyzer.analyze(
                            collected_data, prompt)
                        logging.info(f"LLM Response: {llm_response}")

                        # Execute actions
                        for action in actions:
                            action.execute(llm_response)
                    else:
                        logging.info(
                            f"No data collected from {watcher_name}. Skipping analysis.")

                    logging.info(
                        f"Waiting {interval} seconds until next cycle for {watcher_name}...")
                    time.sleep(interval)

                except Exception as e:
                    logging.error(f"An error occurred during the {watcher_name} cycle: {e}")
                    time.sleep(watcher_info.get('interval', 10))  # Wait before retrying

    except KeyboardInterrupt:
        logging.info("Monitoring stopped.")


if __name__ == "__main__":
    main()
