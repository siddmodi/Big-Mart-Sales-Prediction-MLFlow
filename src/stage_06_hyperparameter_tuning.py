import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from sklearn.model_selection import RandomizedSearchCV
from sklearn.pipeline import Pipeline
from src.stage_05_ct_and_pipeline import pipe2
from src.stage_04_train_test_split import x_train , y_train

STAGE = "HYPERPARAMETER TUNING" ## <<< change stage name 

logging.basicConfig(
    filename=os.path.join("logs", 'running_logs.log'), 
    level=logging.INFO, 
    format="[%(asctime)s: %(levelname)s: %(module)s]: %(message)s",
    filemode="a"
    )


def main(config_path,params_path):
    ## read config files
    config = read_yaml(config_path)
    params = read_yaml(params_path)

    # gridsearchcv
    params = {
        'model__n_estimators'     : params['hyperparameter_tuning']['model__n_estimators'],
        'model__min_samples_split': params['hyperparameter_tuning']['model__min_samples_split'],
        'model__max_depth'        : params['hyperparameter_tuning']['model__max_depth'],
        'model__max_features'     : params['hyperparameter_tuning']['model__max_features'],
        'model__subsample'        : params['hyperparameter_tuning']['model__subsample'],
        'model__min_samples_split': params['hyperparameter_tuning']['model__min_samples_split'],
        'model__min_samples_leaf' : params['hyperparameter_tuning']['model__min_samples_leaf']
        }

    try:
        random_search = RandomizedSearchCV(pipe2, params, cv=params['cv'] , scoring=params['scoring'])
        random_search.fit(x_train, y_train)
    except Exception as e:
        logging.exception(f'Error occured {e}')

    best_params = random_search.best_params_

    logging.info(best_params)
    logging.info(random_search.best_score_)


if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs/config.yaml")
    args.add_argument("--params", "-p", default="params.yaml")
    parsed_args = args.parse_args()

    try:
        logging.info("\n********************")
        logging.info(f">>>>> stage {STAGE} started <<<<<")
        main(config_path=parsed_args.config, params_path=parsed_args.params)
        logging.info(f">>>>> stage {STAGE} completed!<<<<<\n")
    except Exception as e:
        logging.exception(e)
        raise e