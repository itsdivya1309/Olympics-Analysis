import pandas as pd

def extract_season(edition):
    if 'Summer' in edition:
        return 'Summer'
    elif 'Winter' in edition:
        return 'Winter'
    else:
        return 'na'

def preprocess(df):

    # Creating season column and filtering summer Olympics
    df['season'] = df['edition'].apply(extract_season)
    df = df[df['season']=='Summer']

    return df


