import os
import sys

import pandas as pd

from src.logger import logging
from src.exception import CustomException


def read_csv_data():
    try:
        file_path = os.path.dirname(__file__)
        csv_path = os.path.join(file_path, "notebooks", "data", "processed" , "cleaned_atm_transactions.csv")
        
        df = pd.read_csv(csv_path)
        return df
    except Exception as e:
        logging.info("Error Occured")
        raise CustomException(e, sys)
