import os
import sys

import pandas as pd

from src.logger import logging
from src.exception import CustomException


def read_csv_data():
    try:
        project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir))
        file_path = os.path.join(project_root, "data", "processed", "cleaned_atm_transactions.csv")
        df = pd.read_csv(file_path)
        return df
    except Exception as e:
        logging.info("Error Occured")
        raise CustomException(e, sys)
