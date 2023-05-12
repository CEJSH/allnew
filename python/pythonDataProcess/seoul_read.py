import pandas as pd

df = pd.read_csv('seoul.csv', encoding='utf-8')
print(df)
print(df['시군구'].unique())
print(df[df['시군구'] == ' 서울특별시 강남구 신사동'])
print(df.loc[(df['시군구'] == ' 서울특별시 강남구 신사동')])
print(df[(df['시군구'] == ' 서울특별시 강남구 신사동') & (df['단지명'] == '삼지')])


newdf = df.set_index(keys=['도로명'], drop=0)
print(newdf)

print('-' * 50)

result = newdf.loc['동일로']
print(result)
count = result.count()
print(count)
print(count.info())