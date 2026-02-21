import os
import sys
from dataclasses import dataclass

from sklearn.ensemble import GradientBoostingRegressor, RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

from src.exception import CustomException
from src.logger import logging
from src.utils import evaluate_models, save_object

HAS_XGBOOST = False
HAS_CATBOOST = False

try:
    from xgboost import XGBRegressor

    HAS_XGBOOST = True
except Exception as e:
    logging.warning(f"XGBoost unavailable, skipping it: {e}")

try:
    from catboost import CatBoostRegressor

    # Compatibility check for current sklearn API expectations.
    HAS_CATBOOST = hasattr(CatBoostRegressor(), "__sklearn_tags__")
    if not HAS_CATBOOST:
        logging.warning("CatBoost imported but is incompatible with current scikit-learn; skipping it.")
except Exception as e:
    logging.warning(f"CatBoost unavailable, skipping it: {e}")


@dataclass
class ModelTrainerConfig:
    trained_model_file_path: str = os.path.join("artifacts", "model.pkl")


class ModelTrainer:
    def __init__(self):
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array, preprocessor_path):
        try:
            logging.info("Splitting training and test input data")
            X_train, y_train, X_test, y_test = (
                train_array[:, :-1],
                train_array[:, -1],
                test_array[:, :-1],
                test_array[:, -1],
            )

            models = {
                "Random Forest": RandomForestRegressor(),
                "Decision Tree": DecisionTreeRegressor(),
                "Gradient Boosting": GradientBoostingRegressor(),
                "Linear Regression": LinearRegression(),
                "K-Neighbors Regressor": KNeighborsRegressor(),
            }

            if HAS_XGBOOST:
                models["XGBRegressor"] = XGBRegressor()
            if HAS_CATBOOST:
                models["CatBoosting Regressor"] = CatBoostRegressor(
                    verbose=False,
                    allow_writing_files=False,
                )

            params = {
                "Random Forest": {
                    "n_estimators": [50, 100],
                    "max_depth": [None, 10, 20],
                },
                "Decision Tree": {
                    "max_depth": [None, 10, 20],
                    "min_samples_split": [2, 5],
                },
                "Gradient Boosting": {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.05, 0.1],
                },
                "Linear Regression": {},
                "K-Neighbors Regressor": {
                    "n_neighbors": [3, 5, 7],
                    "weights": ["uniform", "distance"],
                },
            }

            if HAS_XGBOOST:
                params["XGBRegressor"] = {
                    "n_estimators": [50, 100],
                    "learning_rate": [0.05, 0.1],
                    "max_depth": [3, 6],
                }
            if HAS_CATBOOST:
                params["CatBoosting Regressor"] = {
                    "iterations": [100, 200],
                    "learning_rate": [0.05, 0.1],
                    "depth": [4, 6],
                }

            model_report: dict = evaluate_models(
                X_train=X_train,
                y_train=y_train,
                X_test=X_test,
                y_test=y_test,
                models=models,
                param=params,
            )

            best_model_score = max(sorted(model_report.values()))

            best_model_name = list(model_report.keys())[list(model_report.values()).index(best_model_score)]
            best_model = models[best_model_name]

            if best_model_score < 0.6:
                raise CustomException("No best model found", sys)

            logging.info(
                f"Best model on training/testing: {best_model_name} with R2 {best_model_score}"
            )

            save_object(
                file_path=self.model_trainer_config.trained_model_file_path,
                obj=best_model,
            )

            predicted = best_model.predict(X_test)
            r2_square = r2_score(y_test, predicted)
            return r2_square

        except Exception as e:
            raise CustomException(e, sys)
