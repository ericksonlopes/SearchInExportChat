import os

from loguru import logger


def setup_logger(_logger=logger):
    """Setup logger"""
    _logger.remove()

    # get current path
    absoulte_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'logs'))

    _logger.add(os.path.join(absoulte_path, 'logs.log'))
    _logger.add(os.path.join(absoulte_path, 'logs_json.log'), serialize=True)

    return _logger
