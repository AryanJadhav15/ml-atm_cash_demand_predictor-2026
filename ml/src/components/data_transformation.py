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
SPLIT_COLUMN = "__dataset_split"


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

            train_df[SPLIT_COLUMN] = "train"
            test_df[SPLIT_COLUMN] = "test"
            combined_df = pd.concat([train_df, test_df], ignore_index=True)
            combined_features = self._create_features(combined_df)

            train_features = combined_features[combined_features[SPLIT_COLUMN] == "train"].drop(
                columns=[SPLIT_COLUMN]
            )
            test_features = combined_features[combined_features[SPLIT_COLUMN] == "test"].drop(
                columns=[SPLIT_COLUMN]
            )

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
        df["hour_sin"] = np.sin(2 * np.pi * df["hour"] / 24)
        df["hour_cos"] = np.cos(2 * np.pi * df["hour"] / 24)

        atm_group = df.groupby("atmId", sort=False)
        df["outcome_lag_1"] = atm_group[TARGET_COLUMN].shift(1)
        df["outcome_lag_2"] = atm_group[TARGET_COLUMN].shift(2)
        df["outcome_lag_3"] = atm_group[TARGET_COLUMN].shift(3)
        df["outcome_lag_6"] = atm_group[TARGET_COLUMN].shift(6)
        df["balance_lag_1"] = atm_group["totalBalance"].shift(1)
        df["transactions_lag_1"] = atm_group["totalNumberTransaction"].shift(1)
        df["rolling_outcome_mean_3"] = atm_group[TARGET_COLUMN].transform(
            lambda values: values.shift(1).rolling(window=3, min_periods=1).mean()
        )
        df["rolling_outcome_mean_6"] = atm_group[TARGET_COLUMN].transform(
            lambda values: values.shift(1).rolling(window=6, min_periods=1).mean()
        )
        df["rolling_outcome_mean_12"] = atm_group[TARGET_COLUMN].transform(
            lambda values: values.shift(1).rolling(window=12, min_periods=1).mean()
        )
        df["rolling_outcome_std_6"] = atm_group[TARGET_COLUMN].transform(
            lambda values: values.shift(1).rolling(window=6, min_periods=2).std()
        )
        df["outcome_trend_3"] = df["outcome_lag_1"] - df["outcome_lag_3"]
        df["balance_trend_3"] = df["balance_lag_1"] - atm_group["totalBalance"].shift(3)

        fill_values = {
            "outcome_lag_1": 0,
            "outcome_lag_2": 0,
            "outcome_lag_3": 0,
            "outcome_lag_6": 0,
            "balance_lag_1": df["totalBalance"].median(),
            "transactions_lag_1": 0,
            "rolling_outcome_mean_3": 0,
            "rolling_outcome_mean_6": 0,
            "rolling_outcome_mean_12": 0,
            "rolling_outcome_std_6": 0,
            "outcome_trend_3": 0,
            "balance_trend_3": 0,
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
