import importlib
import logging
import threading
import time

import yaml
from analyzers.ollama import OllamaAnalyzer
from config import Config
from pydantic import ValidationError

# Configure logging
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def _load_plugin(plugin_type, plugin_config):
    """Dynamically load a watcher or action plugin."""
    plugin_name = None
    try:
        plugin_name = plugin_config.name
        module_name = f"{plugin_type}s.{plugin_name.replace('_watcher', '').replace('_action', '')}"
        class_name = ''.join(word.capitalize()
                             for word in plugin_name.split('_'))

        module = importlib.import_module(module_name)
        plugin_class = getattr(module, class_name)

        return plugin_class(plugin_config)
    except (ImportError, AttributeError) as e:
        logging.error(f"Failed to load plugin: {plugin_name} ({e})")
        return None


def load_config(config_path="config.yaml") -> Config | None:
    """Load and validate the configuration from a YAML file."""
    try:
        with open(config_path, 'r') as f:
            config_data = yaml.safe_load(f)
            return Config.model_validate(config_data)
    except FileNotFoundError:
        logging.error(f"Configuration file '{config_path}' not found.")
        return None
    except (yaml.YAMLError, ValidationError) as e:
        logging.error(f"Error parsing or validating YAML configuration: {e}")
        return None


def main():
    config = load_config()
    if not config:
        exit(1)

    watchers = {}
    for watcher_config in config.watchers:
        if watcher_config.enabled:
            instance = _load_plugin("watcher", watcher_config)
            if instance:
                watcher_name = watcher_config.name
                watchers[watcher_name] = {
                    'instance': instance,
                    'interval': watcher_config.interval_seconds,
                    'prompt': watcher_config.prompt
                }
                logging.info(
                    f"'{watcher_name}' initialized with interval: {watchers[watcher_name]['interval']}s")

    if not watchers:
        logging.info("No active watchers found in the configuration. Exiting.")
        return

    actions = []
    for action_config in config.actions:
        if action_config.enabled:
            instance = _load_plugin("action", action_config)
            if instance:
                actions.append(instance)
                logging.info(f"'{action_config.name}' initialized.")

    if not actions:
        logging.info("No active actions found in the configuration. Exiting.")
        return

    ollama_analyzer = OllamaAnalyzer(config)

    stop_event = threading.Event()

    def watcher_loop(watcher_name, watcher_info, stop_event):
        while not stop_event.is_set():
            try:
                logging.info(f"--- Starting cycle for {watcher_name} ---")
                watcher_instance = watcher_info['instance']
                interval = watcher_info['interval']
                prompt = watcher_info['prompt']

                collected_data = watcher_instance.watch()

                if collected_data:
                    llm_response = ollama_analyzer.analyze(
                        collected_data, prompt)
                    logging.info(f"LLM Response: {llm_response}")

                    for action in actions:
                        action.execute(llm_response)
                else:
                    logging.info(
                        f"No data collected from {watcher_name}. Skipping analysis.")

                for _ in range(interval):
                    if stop_event.is_set():
                        break
                    time.sleep(1)

            except Exception as e:
                logging.error(
                    f"An error occurred during the {watcher_name} cycle: {e}")
                time.sleep(watcher_info.get('interval', 10))

        logging.info(f"{watcher_name} thread exiting...")

    threads = []
    for watcher_name, watcher_info in watchers.items():
        thread = threading.Thread(
            target=watcher_loop, args=(watcher_name, watcher_info, stop_event))
        thread.start()
        threads.append(thread)

    logging.info("Monitoring started. Press Ctrl+C to exit.")

    try:
        while any(thread.is_alive() for thread in threads):
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupt received. Stopping monitoring...")
        stop_event.set()
        for thread in threads:
            thread.join()

    logging.info("All threads stopped. Exiting.")


if __name__ == "__main__":
    main()
