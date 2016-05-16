import pandas as pd
import numpy as np
import datetime

### Convert the timestamp column to a datetime value 
def dateparse (ts):    
        return datetime.datetime.fromtimestamp(float(ts))

### Load the CSV files specifying which is the datetime column and the parse function
df_train = pd.read_csv('../data/train.csv', parse_dates=['time'], date_parser=dateparse)
#df_test = pd.read_csv('../data/test.csv', parse_dates=['time'], date_parser=dateparse)

place_counts = df_train['place_id'].value_counts()
top_places = place_counts.head().index
df_sample = df_train[df_train['place_id'].isin(top_places)]

df_sample.to_csv('../data/top_places.csv', index=False)
