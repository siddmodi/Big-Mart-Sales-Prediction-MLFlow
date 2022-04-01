import argparse
import os
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml, create_directories
import random

from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OrdinalEncoder
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV
from sklearn.metrics import mean_absolute_error , mean_squared_error , r2_score 
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import RandomizedSearchCV
from sklearn.ensemble import GradientBoostingRegressor
# for adj r2 score, Adj r2 = 1-(1-R2)*(n-1)/(n-p-1)


STAGE = "COLUMN TRANSFORMER AND PIPELINE" ## <<< change stage name 

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
        pipe1 = Pipeline([
                ('si',SimpleImputer(strategy='most_frequent',add_indicator=False)),   # Outlet_Size
                ('oe',OrdinalEncoder(categories=[['Small','Medium','High']]))         # Outlet_Size
            ])
        logging.info(f'Pipeline_1 Created : {pipe1}')

    except Exception as e:
        logging.exception(f'Error occured {e}')
    
    try:
        ct = ColumnTransformer(transformers=[
            ('ct1',pipe1,[5]),                                                      # Pipeline :- Outlet_Size
            ('ct2',OrdinalEncoder(categories=[['low fat','regular']]),[1]),        # Item_Fat_Content
            ('ct3',OneHotEncoder(drop='first',handle_unknown = 'ignore'),[3,7]),   # Item_Type , Outlet_Type
            ('ct4',OrdinalEncoder(categories=[['Tier 1','Tier 2','Tier 3']]),[6]), # Outlet_Location_Type
            ('ct5',StandardScaler(),[0,4])                                         # Weight , MRP
        ],remainder='passthrough')   
        logging.info(f'Column Transformer Created : {ct}')

    except Exception as e:
        logging.exception(f'Error occured {e}')

    try:
        pipe2 = Pipeline([
                            ('columnTransformer', ct),
                            ('model', GradientBoostingRegressor())
                        ])
        logging.info(f'Model_Pipeline Created : {pipe2}')
        return pipe2
    
    except Exception as e:
        logging.exception(f'Error occured {e}')

    
    # we choose GradientBoostingRegressor
    # without considering [Outlet_Establishment_Year] col , outlier treatment in ['Item_Weight','Item_MRP'] and /
    # treating less cat as others in [Item_Type]

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