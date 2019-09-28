import pandas as pd
#import numpy as np
#import seaborn as sns
#import matplotlib.pyplot as plt
#%matplotlib inline
#from collections import Counter
#import itertools
#import ast
#import warnings

#import xgboost as xgb
#import catboost as cat
#import lightgbm as lgb

#from scipy.stats import norm, skew
#from sklearn.model_selection import train_test_split, KFold, GroupKFold, StratifiedKFold, cross_validate, cross_val_score
#from sklearn.decomposition import PCA#, TruncatedSVD
#from sklearn.preprocessing import Normalizer, LabelEncoder, OneHotEncoder, FunctionTransformer, StandardScaler, MinMaxScaler, Imputer

#from sklearn.pipeline import make_pipeline, Pipeline
#from sklearn.metrics import mean_squared_error
#from sklearn.ensemble import RandomForestRegressor, ExtraTreesClassifier
#from sklearn.datasets import make_classification

#from sklearn.neighbors import KNeighborsRegressor
#from functools import reduce
#from sklearn import (datasets,discriminant_analysis, neighbors)
#from sklearn.linear_model import LinearRegression#, ElasticNetCV

import json
#import operator
#import time
#import os

warnings.filterwarnings("ignore")
pd.set_option("display.max_columns",100)

seed = 42

#load data

towns = pd.read_json(r'data\towns\towns.json', encoding = 'utf-8')
category = pd.read_json (r'data\guidle\category.json', encoding = 'utf-8')
event = pd.read_json (r'data\guidle\event.json', encoding = 'utf-8')
event_cat = pd.read_json (r'data\guidle\event_category.json', encoding = 'utf-8')

#merge to one full dataframe
event = pd.merge(event, event_cat, how='left', on='event_id')
df = pd.merge(event, category, how='left', on='category_id')

#drop some columns I won't be analysing at the moment / make small version
#df_short = df_full[['event_id','title_en_x','address_city','date', 'start_time', 'end_time', 'price_information', 'short_description_en','long_description_en','title_en_y','parent_category_id']].copy()

df.fillna('',inplace=True)

#look at the data

df.info()
df.head(50)

#df.groupby('title_en_y').count().sort_values('event_id', ascending=False)

#exhibitions, Arts, Sightseeing & city tour, Sport, History, Stage, Museums & attractions,
#Knowledge, computer science & environment

recreation_types = ['hiking', 'skiing', 'biking', 'watersports', 'wellness', 'shopping', 'panorama_trips', 'city_trips', 'nature_and_parks', 'culture']
# -> cities will have these as dummy categories

event_types = ['exhibitions', 'sightseeing', 'sport', 'museums', 'science', 'gastronomy', 'concerts', 'fair_and_market']
# -> events will have these as dummy categories


# -> keywords feature with list of searchable strings

#   two dfs: merged event-df and cities-recreation-info-df, these will be compared with traveltime api

#user can search for a either a regular or a railaway surprise_me destination.
#in either case: mark the event/recreation options they're interested in, give time and price,
#also searchable by travle distance, in which case will check with travel distance api using the towns df
#speech-to-text option. the strings sentences are first checked against the recreation_types, then the event_types and its keywords
#could get city recreation keywords to associate with each category


# re-categorize events

event_cat = {
    'exhibitions': ['Exhibitions', 'Arts', 'Other exhibitions', 'Art & design', 'Permanent exhibition',
                    'Special exhibition'],
    'sightseeing': ['Sightseeing & city tour', 'Excursion'],
    'sport': ['Sports'],
    'museums': ['History', 'Museums & Attractions', 'Other museum & attraction', 'Permanent exhibition',
                'Special exhibition'],
    'science': ['Knowledge, computer science & environment', 'Nature / Environment', 'Cooking, Food & Taste'],
    'gastronomy': ['Culinary art', 'Special food offers', 'More Food Specials'],
    'concerts': ['Concerts others', 'Other music ads', 'Stage'],
    'fair_and_market': ['Fair & market', 'Crafts / Gold / jewelry / fashion', 'Society', 'Man / society']
}

text_cols = ['long_description_de', 'long_description_en',
             'long_description_fr', 'long_description_it', 'price_information',
             'short_description_de', 'short_description_en', 'short_description_fr',
             'short_description_it', 'title_de_x',
             'title_en_x', 'title_fr_x', 'title_it_x', 'title_de_y', 'title_en_y', 'title_fr_y',
             'title_it_y']


def get_cats(d):
    # Change overview into list of lower case words, get rid of non-alphanumeric characters.
    # i=short_description_en
    # d.loc[d[i].notnull(),i]=d.loc[d[i].notnull(),i].apply(lambda x : [''.join(ch for ch in y if ch.isalnum()).lower() for y in str(x).split(' ')])
    # d['len_overview']= d[i].apply(lambda x:len(x) if x!=0 else 0)

    for i in event_types:
        d[i] = d.title_en_y.apply(lambda x: x in event_cat[i])

    for col in text_cols:
        d.loc[d[col].notnull(), col] = d.loc[d[i].notnull(), col].apply(
            lambda x: [''.join(ch for ch in y if ch.isalnum()).lower() for y in str(x).split(' ')])

    # d['overview'] = d.title_en_y.apply(lambda x: [''.join(ch for ch in y if ch.isalnum()).lower() for y in str(x).split(' ')])

    # rename some stuff, drop unnecessary categories
    # d.rename(columns = {'':'','':'','':''},inplace = True)

    # d.index = d['']

    # d = d.drop(['','',''],axis=1)

    return d


df = get_cats(df)

df.to_json(path_or_buf='event_data.json')#, encoding = 'utf-8')
