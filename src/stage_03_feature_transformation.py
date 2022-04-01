import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df
from src.utils.feature_transformation import naming_as_others_for_less_frequent_value


STAGE = "FEATURE TRANSFORMATION" ## <<< change stage name 

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

    #df['Item_Weight'] = df['Item_Weight'].astype(float)

    try:
        df['Item_Fat_Content'].replace(to_replace={'LF':'low fat' ,'Low Fat':'low fat' , 'Regular':'regular' , 'reg':'regular' },inplace=True)
    except Exception as e:
        logging.exception(f'Error occured {e}')

    # naming less frequent Item_Type as others (having value counts less than 4% of total values)
    try:
        naming_as_others_for_less_frequent_value(df,
                                            column='Item_Type',
                                            threshold = 4)
    except Exception as e:
        logging.exception(f'Error occured {e}')

    # Drop Columns
    try:
        df.drop(['Item_Identifier','Outlet_Identifier','Outlet_Establishment_Year'],axis=1,inplace=True)
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