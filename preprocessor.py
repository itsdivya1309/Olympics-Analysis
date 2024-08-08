import pandas as pd

def extract_season(edition):
    if 'Summer' in edition:
        return 'Summer'
    elif 'Winter' in edition:
        return 'Winter'
    else:
        return 'na'

def preprocess(medals):

    # Creating season column and filtering summer Olympics
    medals['season'] = medals['edition'].apply(extract_season)
    medals = medals[medals['season']=='Summer']

    return medals


