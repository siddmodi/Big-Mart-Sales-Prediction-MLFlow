import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random
from src.stage_01_get_data import df
from src.utils.missing_values import fill_missing_with_mode
from Dataframe import  df


STAGE = "HANDLING MISSING VALUES" ## <<< change stage name 

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

    # Outlet_Size         
    try:
        fill_missing_with_mode(df,'Outlet_Size')
        logging.info('Outlet_Size missing values filled with mode')
    except Exception as e:
        logging.exception(f'Error Occured : {e}')

    # Item_Weight

    df2=df[['Item_Identifier','Item_Weight']]
    try:
        dfx=df2.drop_duplicates()
        dfx=dfx.dropna()
        dfx.set_index('Item_Identifier',inplace=True)
        df['Item_Weight']=df['Item_Weight'].astype(str)

        for i,r in df.iterrows():
            if r['Item_Weight'] =='nan':
                df['Item_Weight'][i]=str(dfx['Item_Weight'][r['Item_Identifier']])
        logging.info('Item_Weight missing values filled')

    except Exception as e:
        logging.exception(f'Error Occured : {e}')
    
 
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