import argparse
import mlflow
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random


STAGE = "MAIN" ## <<< change stage name 

create_directories(["logs"])
with open(os.path.join("logs", 'running_logs.log'), "w") as f:
    f.write("")

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path):
    with mlflow.start_run() as run:
        mlflow.run(".", "get_data", use_conda=False)
        # mlflow.run(".", "get_data", parameters={}, use_conda=False)
        mlflow.run(".", "handling_missing_values", use_conda=False)
        mlflow.run(".", "feature_transformation", use_conda=False)
        mlflow.run(".", "train_test_split", use_conda=False)
        mlflow.run(".", "ct_and_pipeline", use_conda=False)
        mlflow.run(".", "hyperparameter_tuning", use_conda=False)
        mlflow.run(".", "pipeline", use_conda=False)

if __name__ == '__main__':
    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main()
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e