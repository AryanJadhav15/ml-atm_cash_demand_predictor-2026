import sys

from src.components.data_ingestion import DataIngestion
from src.components.data_transformation import DataTransformation
from src.components.model_trainer import ModelTrainer
from src.exception import CustomException
from src.logger import logging


class TrainPipeline:
    def run(self):
        try:
            train_path, test_path = DataIngestion().initiate_data_ingestion()
            train_arr, test_arr, _ = DataTransformation().initiate_data_transformation(
                train_path,
                test_path,
            )
            metrics = ModelTrainer().initiate_model_trainer(train_arr, test_arr)
            logging.info("Training pipeline completed")
            return metrics
        except Exception as e:
            logging.info("Error Occured in training pipeline")
            raise CustomException(e, sys)
