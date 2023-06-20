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

    df_tl['END_RANGE_HOSP'] = df_tl['DAY'].copy()
    df_tl['END_RANGE_FALL'] = df_tl['DAY'].copy()
    df_tl['END_RANGE_PAIN'] = df_tl['DAY'].copy()

    # change True/False to int, with real data would maybe have count
    df_tl['HAS_PAIN_MENTION'] = df_tl['HAS_PAIN_MENTION'].astype(int)

    # add column for timeline x_end
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

