import os
import sys
import json

import joblib
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


def save_object(file_path, obj):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        joblib.dump(obj, file_path)
    except Exception as e:
        logging.info("Error Occured while saving object")
        raise CustomException(e, sys)


def load_object(file_path):
    try:
        return joblib.load(file_path)
    except Exception as e:
        logging.info("Error Occured while loading object")
        raise CustomException(e, sys)


def save_json(file_path, data):
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
    except Exception as e:
        logging.info("Error Occured while saving json")
        raise CustomException(e, sys)
