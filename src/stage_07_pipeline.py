import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
from sklearn.pipeline import Pipeline
from sklearn.ensemble import GradientBoostingRegressor
from src.stage_05_ct_and_pipeline import ct
import joblib
from src.stage_04_train_test_split import x_train , y_train
from src.stage_06_hyperparameter_tuning import best_params
from src.utils.common import create_directories
import random


STAGE = "PIPELINE" ## <<< change stage name 

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

    l=[]
    for i in best_params.values():
        l.append(i)

    try:
        pipeline = Pipeline([
                            ('columnTransformer', ct),
                            ('model', GradientBoostingRegressor(max_depth=l[0] ,
                                                                max_features=l[1] ,
                                                                min_samples_leaf=l[2] ,
                                                                min_samples_split=l[3] ,
                                                                n_estimators=l[4] ,
                                                                subsample=l[5]))
                            ])
        logging.info(f'Pipeline created {pipeline}')

    except Exception as e:
        logging.exception(f'Error occured {e}')

    try:
        pipeline.fit(x_train,y_train)
        logging.info(f'Pipeline Trained succesfully')

    except Exception as e:
        logging.exception(f'Pipeline does not Trained/n Error occured : {e}')

    if os.path.exists(pipeline_dir)==False:
        pipeline_dir = create_directories(config['data']['pipeline_dir'])
        pipeline_joblib = os.path.join(pipeline_dir,
                                    config['data']['pipeline_file'])
        joblib.dump(pipeline, pipeline_joblib)  
        logging.info(f"Trained pipeline is saved at : {pipeline_dir}")
        return pipeline
    else:
        logging.info(f'Trained Pipeline already present in {pipeline_dir}')


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