import pandas as pd
import logging

def naming_as_others_for_less_frequent_value(dataframe,column,threshold=4):
    '''
        --------------------------
    '''
    try:
        arr_others = dataframe[column].value_counts()[dataframe[column].value_counts(normalize=True)*100 < threshold].index
        dataframe[column].replace(to_replace=arr_others, value = ['others']*len(arr_others), inplace=True)    
    except Exception as e:
        logging.exception(f'Error occured {e}')


# In all function do 3 things
# Dockstring --> function kya kr rha h and inputs kya maang rha h kese
# () bracket me mention kro jese sir ne kia h 