import sys
import os

import pandas as pd
from dataclasses import dataclass

from src.logger import logging
from src.exception import CustomException
from src.utils import read_csv_data

@dataclass
class DataIngestionConfig:
    raw_data_path: str = os.path.join("artifacts", "raw_data.csv")
    train_data_path: str = os.path.join("artifacts","train_data.csv")
    test_data_path: str = os.path.join("artifacts","test_data.csv")
    test_size: float = 0.2
    
class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
    
    def initiate_data_ingestion(self):
        try:
            df = read_csv_data()
            logging.info("Data Reading Complete")

            os.makedirs(os.path.dirname(self.ingestion_config.raw_data_path), exist_ok=True)

            df["transactionTime"] = pd.to_datetime(df["transactionTime"], errors="raise")
            df = df.sort_values(["transactionTime", "atmId"]).reset_index(drop=True)
            
            df.to_csv(self.ingestion_config.raw_data_path, index=False)
            logging.info("raw data added to artifacts")

            split_index = int(len(df) * (1 - self.ingestion_config.test_size))
            train_set = df.iloc[:split_index].copy()
            test_set = df.iloc[split_index:].copy()
            logging.info("time-based train test split complete")
            
            train_set.to_csv(self.ingestion_config.train_data_path, index=False)
            test_set.to_csv(self.ingestion_config.test_data_path, index=False)
            logging.info("train_set and test_set added in artifacts")

            return (
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path,
            )
        except Exception as e:
            logging.info("Error Occured")
            raise CustomException(e, sys)
