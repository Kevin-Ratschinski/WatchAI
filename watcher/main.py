import logging

# setup basic logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s -%(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
logger = logging.getLogger('watcher')


def main():
    print("Hello from watcher!")


if __name__ == "__main__":
    main()
