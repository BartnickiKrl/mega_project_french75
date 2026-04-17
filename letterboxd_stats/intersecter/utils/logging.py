import logging
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo


def get_logger(name: str, level: int = logging.INFO, log_dir: Path = Path("logs")):
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(level)
    timestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%H:%M:%S")
    formatter = logging.Formatter(f"{timestamp} %(name)s - %(levelname)s - %(message)s")

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    Path(log_dir).mkdir(exist_ok=True)
    datestamp = datetime.now(ZoneInfo("Europe/Warsaw")).strftime("%d-%m-%Y")


    file_handler = logging.FileHandler(
        f"{log_dir}/app_{datestamp}.log", encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger
