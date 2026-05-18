import sys

from src.logger import logging
from src.exception import CustomException
from src.pipelines.train_pipeline import TrainPipeline


if __name__ == "__main__":
    try:
        metrics = TrainPipeline().run()
        logging.info(f"Training completed. Metrics: {metrics}")
    except Exception as e:
        logging.info("Error Occured")
        raise CustomException(e, sys)
