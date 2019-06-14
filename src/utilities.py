"""
module for various utilities
"""
import logging

def config_logging():
    logging.basicConfig(
                        format='%(message)s',
                        level=logging.DEBUG)
    logging.getLogger().setLevel(logging.INFO)
    logger = logging.getLogger('')
    logger.handlers = []
