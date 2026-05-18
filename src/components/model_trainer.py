import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

from src.exception import CustomException
from src.logger import logging
from src.utils import save_json, save_object


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.joblib")
    metrics_file_path: str = os.path.join("artifacts", "metrics.json")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            x_train, y_train = train_array[:, :-1], train_array[:, -1]
            x_test, y_test = test_array[:, :-1], test_array[:, -1]

            model = RandomForestRegressor(
                n_estimators=200,
                min_samples_leaf=2,
                random_state=42,
                n_jobs=-1,
            )
            model.fit(x_train, y_train)

            predictions = model.predict(x_test)
            metrics = {
                "mae": float(mean_absolute_error(y_test, predictions)),
                "rmse": float(mean_squared_error(y_test, predictions) ** 0.5),
                "r2_score": float(r2_score(y_test, predictions)),
            }

            save_object(self.model_trainer_config.trained_model_file_path, model)
            save_json(self.model_trainer_config.metrics_file_path, metrics)

            logging.info("Saved model and evaluation metrics")
            return metrics
        except Exception as e:
            logging.info("Error Occured in model training")
            raise CustomException(e, sys)
