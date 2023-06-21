# Testing testing

import pandas as pd
from datetime import timedelta, date
import datetime
import numpy as np
from utils import *


def preprocess_general_timeline(df_tl):

    # sort names in alphabetical order and reset index
    df_tl.sort_values('PATIENT_ID', ascending=False, inplace=True)
    df_tl.reset_index(drop=True, inplace=True)

    # convert to datetime format
    df_tl['DAY'] = pd.to_datetime(df_tl['DAY'])

    # change True/False to int, with real data would maybe have count
    df_tl['HAS_PAIN_MENTION'] = df_tl['HAS_PAIN_MENTION'].astype(int)

    # add column for timeline x_end
    df_tl['END_RANGE_HOSP'] = df_tl['DAY'].copy()
    df_tl['END_RANGE_FALL'] = df_tl['DAY'].copy()
    df_tl['END_RANGE_PAIN'] = df_tl['DAY'].copy()
    
    df_tl.loc[list(df_tl.loc[df_tl['HOSPITALIZATION_COUNT']!=0].index.values),'END_RANGE_HOSP'] += timedelta(days=1)
    df_tl.loc[list(df_tl.loc[df_tl['FALL_COUNT']!=0].index.values),'END_RANGE_FALL'] += timedelta(days=1)
    df_tl.loc[list(df_tl.loc[df_tl['HAS_PAIN_MENTION']!=0].index.values),'END_RANGE_PAIN'] += timedelta(days=1)
    
    # convert details into desired formats
    df_tl['HOSPITALIZATION_TIME'] = df_tl['HOSPITALIZATION_DETAILS'].apply(lambda x: convert_detail_time(x) if x!='0' else 0)
    df_tl['HOSPITALIZATION_SOURCE'] = df_tl['HOSPITALIZATION_DETAILS'].apply(lambda x: convert_detail_source(x) if x!='0' else 0)

    df_tl['FALL_TIME'] = df_tl['FALL_DETAILS'].apply(lambda x: convert_detail_time(x) if x!='0' else 0)
    df_tl['FALL_SOURCE'] = df_tl['FALL_DETAILS'].apply(lambda x: convert_detail_source(x) if x!='0' else 0)

    df_tl['PAIN_TIME'] = df_tl['PAIN_DETAILS'].apply(lambda x: convert_detail_time(x) if x!='[]' else 0)
    df_tl['PAIN_SOURCE'] = df_tl['PAIN_DETAILS'].apply(lambda x: convert_detail_source(x) if x!='[]' else 0)
    
    return df_tl

'''
    Contains some functions to preprocess the data used in the visualisation.
'''

import pandas as pd

def round_decimals(my_df):
    '''
        Rounds all the numbers in the dataframe to two decimal points

        args:
            my_df: The dataframe to preprocess
        returns:
            The dataframe with rounded numbers
    '''
    return my_df.round(2)


def get_range(col, df1, df2):
    '''
        An array containing the minimum and maximum values for the given
        column in the two dataframes.

        args:
            col: The name of the column for which we want the range
            df1: The first dataframe containing a column with the given name
            df2: The first dataframe containing a column with the given name
        returns:
            The minimum and maximum values across the two dataframes
    '''
    if min(df1[col]) < min(df2[col]):
        min_ = min(df1[col])
    else:
        min_ = min(df2[col])
        
    if max(df1[col]) > max(df2[col]):
        max_ = max(df1[col])
    else:
        max_ = max(df2[col])
        
    return [min_, max_]


def combine_dfs(df1, df2):
    '''
        Combines the two dataframes, adding a column 'Year' with the
        value 2000 for the rows from the first dataframe and the value
        2015 for the rows from the second dataframe

        args:
            df1: The first dataframe to combine
            df2: The second dataframe, to be appended to the first
        returns:
            The dataframe containing both dataframes provided as arg.
            Each row of the resulting dataframe has a column 'Year'
            containing the value 2000 or 2015, depending on its
            original dataframe.
    '''
    # We add the 'Year' column to each individual dataframe
    year_2000 = [2000] * len(df1)
    year_2015 = [2015] * len(df2)
    df1['Year'] = year_2000
    df2['Year'] = year_2015

    # We concatenate the two dataframes
    df = pd.concat([df1, df2], ignore_index=True)

    return df


def sort_dy_by_yr_continent(my_df):
    '''
        Sorts the dataframe by year and then by continent.

        args:
            my_df: The dataframe to sort
        returns:
            The sorted dataframe.
    '''
    return my_df.sort_values(['Year', 'Continent'])