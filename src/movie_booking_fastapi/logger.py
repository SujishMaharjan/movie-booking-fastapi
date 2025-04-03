import logging
from logging.handlers import RotatingFileHandler

class CustomLog:

    def __init__(self, name=__name__, log_file="logs/app.log",level=logging.DEBUG):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "{asctime} - {levelname} - {message}",
            style = "{",
            datefmt = "%Y-%m-%d %H:%M"
        )

        #Console Handler
        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        #File Handler
        file_handler = RotatingFileHandler(log_file, maxBytes=1000, backupCount=5)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)


    def get_logger(self):
        return self.logger
    

logger = CustomLog().get_logger()






