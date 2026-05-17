import sys
import os

import pandas as pd
from dataclasses import dataclass
from sklearn.model_selection import train_test_split

from src.logger import logging
from src.exception import CustomException
from src.utils import read_csv_data

@dataclass
class DataIngestionConfig():
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("artifacts","train_data.csv")
    test_data_path: str = os.path.join("artifacts","test_data.csv")
    
class DataIngestion():
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        try:
            df = read_csv_data()
            logging.info("Data Reading Complete")
            
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("raw data added to artifacts")
            
            train_set, test_set = train_test_split(df, test_size=0.2, random_state=42)
            logging.info("train_test_split complete")
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("train_set and test_set added in artifacts")
            
            
        except Exception as e:
            logging.info("Error Occured")
            raise CustomException(e, sys)

