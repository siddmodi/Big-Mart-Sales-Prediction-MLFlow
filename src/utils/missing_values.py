import logging
import pandas as pd


def fill_missing_with_mode(dataframe,column_name):
    try:
        dataframe[column_name].fillna(dataframe[column_name].mode()[0], inplace=True)
    except Exception as e:
        logging.exception(f'Error occured {e}')    