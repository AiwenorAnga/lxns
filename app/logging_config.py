# logging_config.py

import logging


def setup_logging():
    logger = logging.getLogger(__name__)
    logging.basicConfig(
        filename="logfile.log",
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
    )
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    return logger


logger = setup_logging()
