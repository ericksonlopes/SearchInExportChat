from loguru import logger


def setup_logger(_logger=logger):
    """Setup logger"""
    _logger.remove()

    _logger.add(f'logs/app.log')
    _logger.add(f'logs/app_json.log', serialize=True)

    return _logger
