import pandas as pd
import numpy as np

sdata = {
    '국어': [60, np.nan, 40],
'영어': [np.nan, 80, 50],
'수학': [90, 50, np.nan]
}
name = ['강감찬','김유신', '이순신']

df = pd.DataFrame(data=sdata, index=name)
print(df)
print(df.mean(axis=0))

df.loc[df['국어'].isnull(), '국어'] = df['국어'].mean()
df.loc[df['영어'].isnull(), '영어'] = df['영어'].mean()
df.loc[df['수학'].isnull(), '수학'] = df['수학'].mean()
print(df)

df_fill = df.fillna(df.mean(axis=0))
print(df_fill)
print(df_fill.describe())