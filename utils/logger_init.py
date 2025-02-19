import logging.config


logging.config.fileConfig("logging.ini")


logger = logging.getLogger()


logger.debug("Test log at DEBUG level")
logger.info("Test log at INFO level")
logger.warning("Test log at WARNING level")
