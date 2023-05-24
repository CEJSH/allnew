import pandas as pd
import numpy as np

df = pd.read_csv("xx_construction_Seocho_10800.csv", encoding='utf-8')

df.drop('Unnamed: 0', axis=1, inplace=True)

#fill empty data with null
df[['착공예정일','착공연기일','실제착공일']] = df[['착공예정일','착공연기일','실제착공일']].replace(" ", np.nan)

# to only see necessary data, if the data has none of '착공예정일' and '실제착공일', drop the data
df.dropna(subset=['착공예정일', '실제착공일'], how='all', axis=0, inplace = True)

# reset index
df = df.reset_index(drop=True)
print(df.info())

# if the space exists, make the data null value.
for i in range(len(df)):
    if df.iloc[i][2] != np.nan:
        if " " in str(df.iloc[i][2]) :
            df.iloc[i][2] = np.nan
    if df.iloc[i][3] != np.nan:
        if " " in str(df.iloc[i][2]) :
            df.iloc[i][3] = np.nan
    if df.iloc[i][4] != np.nan:
        if " " in str(df.iloc[i][2]) :
            df.iloc[i][4] = np.nan

# make the data type into float for comparing
df[['착공예정일','착공연기일','실제착공일']] = df[['착공예정일','착공연기일','실제착공일']].astype('float')

# the code below is not available when the range was given only len(df) or len(df)-1 beacuse droping index was affecting total amount of indexs 
for i in range(len(df)-1,-1,-1):
    if not pd.isnull(df.iloc[i][2]) and df.iloc[i][2] < 20221201:
            df.drop(index=i, axis=0, inplace=True)
    elif not pd.isnull(df.iloc[i][3]) and df.iloc[i][3] < 20221201:
            df.drop(index=i, axis=0,inplace=True)
    elif not pd.isnull(df.iloc[i][4]) and df.iloc[i][4] < 20221201:
            df.drop(index=i,axis=0, inplace=True)
# reset index
df = df.reset_index(drop=True)
print(df.info())

# index_con = df[df['대지위치'] == '서울특별시 강남구 역삼동 605-26번지'].index
# df.drop(index_con, inplace=True)
# df[['착공예정일','착공연기일','실제착공일']] = df[['착공예정일','착공연기일','실제착공일']].astype('float')
# df = df.reset_index(drop=True)
print(df)
df.to_csv("Seocho_seocho.csv")