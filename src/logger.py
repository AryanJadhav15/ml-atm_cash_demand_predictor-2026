import os
import logging
from datetime import datetime

LOG_FILE_NAME = f"{datetime.now().strftime("%d_%m_%Y_%H_%M_%S")}.log"

log_file_path = os.path.join("logs", LOG_FILE_NAME)

logging.basicConfig(
    filename=log_file_path,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)