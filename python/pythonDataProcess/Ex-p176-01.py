import pandas as pd

mylist = [200, 300,4000, 100]
myseries = pd.Series(data = mylist, index = ['손오공', '저팔계', '사오정', '삼장법사'])

myseries.index.name = '실적 현황'
print('\nindex name of series')
print(myseries.index.name)

myseries.name = '직원 실적'
print('\nname of series')
print(myseries.name)
print(myseries)

print('\n# 반복하여 출력해보기')
for idx in myseries.index:
    print('색인 : ' + idx + ' , 값 : ' + str(myseries[idx]))