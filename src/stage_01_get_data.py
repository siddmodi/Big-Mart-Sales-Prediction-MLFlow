import argparse
import os
import pandas as pd
import shutil
from tqdm import tqdm
import logging
from src.utils.common import read_yaml
import random
import cassandra
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import yaml

STAGE = "GET DATA" ## <<< change stage name 

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
    path_for_bundle = config['cassandra_db']['source_url']
    client_id = config['cassandra_db']['client_id']
    client_secret = config['cassandra_db']['client_secret']

    cloud_config= {
            'secure_connect_bundle': path_for_bundle
                    }
    auth_provider = PlainTextAuthProvider(client_id,client_secret)
    cluster = Cluster(cloud=cloud_config, auth_provider=auth_provider)
    session = cluster.connect()
    row = session.execute("select release_version from system.local").one()
    if row:
        logging.info(row[0]+' and connection establish')
    else:
        logging.info("An error occurred.")

    try:
        row=session.execute("use ks_sales;")
        df =pd.DataFrame(data=session.execute("select * from tb_sales;"))
        df.drop(['key'],axis=1,inplace=True)

        
        if os.path.exists(df_dir)==False:
            df_dir = os.makedirs(config['data']['df_dir'])
            df_path = os.path.join(config['data']['df_dir'],
                            config['data']['df_file'])
            df.to_csv(df_path,index=False)
            logging.info(f'Save Dataframe {df} to {df_path}')
            df = pd.read_csv(df_path,index_col=[0])
            logging.info(f'We get Dataframe name df : {df}')
        else:
            logging.info(f'Dataframe {df} already present in {df_dir}')

    except Exception as e:
        logging.exception(f'Error occured while taking dataframe {e}')
        raise e

if __name__ == '__main__':
    args = argparse.ArgumentParser()
    args.add_argument("--config", "-c", default="configs\config.yaml")
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


# TO RUN THIS PY FILE 
# python src\stage_01_get_data.py --config="configs\config.yaml"