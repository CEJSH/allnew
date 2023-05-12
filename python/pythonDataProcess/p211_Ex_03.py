import pandas as pd
import numpy as np

filename = '과일매출현황.csv'

df = pd.read_csv(filename, encoding='utf-8', index_col='과일명')
print(df)

df2 = df.fillna({'구입액': 50, '수입량': 20})
print(df2)

print('# 구입액과 수입량의 각 소계')
print(df2.sum(axis=0))

print('# 과일별 소계')
print(df2.sum(axis=1))

print('# 구입액과 수입량의 평균')
print(df2.mean(axis=0))

print('# 과일별 평균')
print(df2.mean(axis=1))