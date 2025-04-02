import logging

def setup_logging():
    logger = logging.getLogger(__name__)
    logger.setLevel('DEBUG')
    formatter = logging.Formatter(
        "{asctime} - {levelname} - {message}",
        style="{",
        datefmt="%Y-%m-%d %H:%M", 
    )

    console_handler = logging.StreamHandler()
    console_handler.setLevel("DEBUG")
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)


    file_handler = logging.FileHandler("app.log", mode="a", encoding="utf-8")
    file_handler.setLevel("DEBUG")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)