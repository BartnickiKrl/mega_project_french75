import logging
from datetime import datetime
from pathlib import Path


def get_logger(name: str, level: int = logging.INFO, log_dir: Path = Path("logs")):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)

    formatter = logging.Formatter("%(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    Path(log_dir).mkdir(exist_ok=True)
    timestamp = datetime.now().strftime("%d-%m-%Y")
    file_handler = logging.FileHandler(
        f"{log_dir}/app_{timestamp}.log", encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
