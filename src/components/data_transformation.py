import os
import sys
from dataclasses import dataclass

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object


TARGET_COLUMN = "totalOutcome"


@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path: str = os.path.join("artifacts", "preprocessor.joblib")


class DataTransformation:
    def __init__(self):
        self.data_transformation_config = DataTransformationConfig()

    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info("Loaded train and test data for transformation")

            train_features = self._create_features(train_df)
            test_features = self._create_features(test_df)

            input_feature_train_df = train_features.drop(columns=[TARGET_COLUMN])
            target_feature_train_df = train_features[TARGET_COLUMN]

            input_feature_test_df = test_features.drop(columns=[TARGET_COLUMN])
            target_feature_test_df = test_features[TARGET_COLUMN]

            preprocessor = self._get_preprocessor_object(input_feature_train_df)

            input_feature_train_arr = preprocessor.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessor.transform(input_feature_test_df)

            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            save_object(
                self.data_transformation_config.preprocessor_obj_file_path,
                preprocessor,
            )

            logging.info("Saved preprocessing object")

            return (
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path,
            )
        except Exception as e:
            logging.info("Error Occured in data transformation")
            raise CustomException(e, sys)

    def _get_preprocessor_object(self, input_df):
        numeric_columns = input_df.select_dtypes(include=["number", "bool"]).columns.tolist()
        categorical_columns = input_df.select_dtypes(include=["object", "category"]).columns.tolist()

        numeric_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="median")),
                ("scaler", StandardScaler()),
            ]
        )

        categorical_pipeline = Pipeline(
            steps=[
                ("imputer", SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder", OneHotEncoder(handle_unknown="ignore", sparse_output=False)),
            ]
        )

        return ColumnTransformer(
            transformers=[
                ("numeric_pipeline", numeric_pipeline, numeric_columns),
                ("categorical_pipeline", categorical_pipeline, categorical_columns),
            ],
            sparse_threshold=0,
        )

    def _create_features(self, df):
        df = df.copy()
        df["transactionTime"] = pd.to_datetime(df["transactionTime"], errors="raise")
        df = df.sort_values(["atmId", "transactionTime"]).reset_index(drop=True)

        df["hour"] = df["transactionTime"].dt.hour
        df["day_of_week"] = df["transactionTime"].dt.dayofweek
        df["month"] = df["transactionTime"].dt.month
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

        atm_group = df.groupby("atmId", sort=False)
        df["previous_total_outcome"] = atm_group[TARGET_COLUMN].shift(1)
        df["previous_total_balance"] = atm_group["totalBalance"].shift(1)
        df["previous_total_transactions"] = atm_group["totalNumberTransaction"].shift(1)
        df["rolling_outcome_mean_3"] = atm_group[TARGET_COLUMN].transform(
            lambda values: values.shift(1).rolling(window=3, min_periods=1).mean()
        )

        fill_values = {
            "previous_total_outcome": 0,
            "previous_total_balance": df["totalBalance"].median(),
            "previous_total_transactions": 0,
            "rolling_outcome_mean_3": 0,
        }
        df = df.fillna(fill_values)

        leakage_columns = [
            "numberIncomeTransaction",
            "numberOutcomeTransaction",
            "totalIncome",
            "totalNumberTransaction",
        ]
        unused_columns = [
            "atmName",
            "atmAddress",
            "transactionTime",
            "day",
        ]

        return df.drop(columns=leakage_columns + unused_columns)
