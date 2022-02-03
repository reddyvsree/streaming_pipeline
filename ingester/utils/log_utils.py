import logging
import argparse


def get_logger(logger_name, log_level='info'):
    levels = {
        'critical': logging.CRITICAL,
        'error': logging.ERROR,
        'warn': logging.WARNING,
        'warning': logging.WARNING,
        'info': logging.INFO,
        'debug': logging.DEBUG,
    }

    parser = argparse.ArgumentParser()
    parser.add_argument('--log', '-log', default='info')
    options = parser.parse_args()
    log_level = options.log.lower()
    level = levels.get(log_level, 'info')

    logger = logging.getLogger(logger_name)
    logger.setLevel(level)
    stdout_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s")
    stdout_handler.setFormatter(formatter)
    logger.addHandler(stdout_handler)
    return logger
