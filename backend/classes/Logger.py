import logging, os

LOG_FILE_URL = "logs/utils_logger.log"


class Logger:
    """
    This module provides a basic logging utility with file and console output support.
    The script automatically sets up a logger with a file handler and a console handler.
    """

    def __init__(self):
        self.log_level = logging.INFO
        self.logger = self.setup_logger()
        self.log_file_path = os.path.abspath(LOG_FILE_URL)

    def setup_logger(self):
        logger = logging.getLogger()
        logger.setLevel(self.log_level)
        file_handler = logging.FileHandler(LOG_FILE_URL, mode="a")
        file_handler.setLevel(self.log_level)
        console_handler = logging.StreamHandler()
        console_handler.setLevel(self.log_level)
        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
        )
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        console_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        return logger

    def log(self, message, level=logging.INFO):
        if level == "INFO":
            self.logger.info(message)
        elif level == "WARNING":
            self.logger.warning(message)
        elif level == "ERROR":
            self.logger.error(message)
        elif level == "CRITICAL":
            self.logger.critical(message)
