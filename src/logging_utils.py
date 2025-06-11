import logging
import sys

def setup_logging(level=logging.INFO):
    """
    Configures basic logging to stdout.

    Args:
        level: The logging level to set for the root logger and console handler.
               Defaults to logging.INFO.
    """
    logger = logging.getLogger()
    logger.setLevel(level)

    # Prevent adding multiple handlers if called multiple times
    if not any(isinstance(h, logging.StreamHandler) and h.stream == sys.stdout for h in logger.handlers):
        ch = logging.StreamHandler(sys.stdout)
        ch.setLevel(level)

        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                                      datefmt='%Y-%m-%d %H:%M:%S')
        ch.setFormatter(formatter)
        logger.addHandler(ch)

if __name__ == '__main__':
    # Example usage:
    setup_logging(logging.DEBUG) # Set to DEBUG for more verbose output for this example

    # Test logging messages
    logging.debug("This is a debug message.")
    logging.info("This is an info message.")
    logging.warning("This is a warning message.")
    logging.error("This is an error message.")
    logging.critical("This is a critical message.")

    # Test logging from a specific module logger
    module_logger = logging.getLogger("MyModule")
    module_logger.info("This is an info message from MyModule.")

    try:
        1 / 0
    except ZeroDivisionError:
        module_logger.exception("A ZeroDivisionError occurred!")
