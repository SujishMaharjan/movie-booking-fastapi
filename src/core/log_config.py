import logging
from logging.handlers import RotatingFileHandler


class MovieLog:
    """
    CustomLog class for setting up logging with both console and file handlers.

    This class initializes a logger with console and rotating file handlers,
    which output logs to the console and a log file respectively.

    Attributes:
        logger (logging.Logger): A logger instance for logging messages.
    """

    def __init__(self, name=__name__, log_file="logs/app.log", level=logging.DEBUG):
        """
        Initializes the logger with console and file handlers.

        Args:
            name (str): The name of the logger. Defaults to the current module name.
            log_file (str): The log file path for the rotating file handler.
            Defaults to "logs/app.log".
            level (int): The logging level. Defaults to logging.DEBUG.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}", style="{", datefmt="%Y-%m-%d %H:%M"
        )

        # Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # File Handler
        file_handler = RotatingFileHandler(log_file, maxBytes=500000, backupCount=5)
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def get_logger(self):
        """
        Return logger instance for logging messages.
        """
        return self.logger


logger = MovieLog().get_logger()
