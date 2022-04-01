import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df
from sklearn.model_selection import train_test_split
import pandas as pd


STAGE = "TRAIN TEST SPLIT" ## <<< change stage name 

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

    try:
        x = df.drop(columns=['Item_Outlet_Sales'])
        y = df['Item_Outlet_Sales']

        x_train, x_test, y_train, y_test = train_test_split(x, y, 
                                                test_size=params['test_size'],
                                                random_state=params['random_state'])

        x_train = x_train.reset_index(drop=True)
        y_train = pd.DataFrame(y_train).reset_index(drop=True)

        logging.info('Train-Test split Done')

    except Exception as e:
        logging.exception(f'Error occured {e}')
    


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