import pandas as pd

myindex01 = ['성춘향', '이몽룡','심봉사']
myindex02 = ['성춘향', '이몽룡','뺑덕어멈']

mylist01 = [40, 50, 60]
mylist02 = [20, 40, 70]

myseries01 = pd.Series(data = mylist01, index=myindex01)
myseries02 = pd.Series(data = mylist02, index=myindex02)
print(myseries01)
print(myseries02)

print('\n# 두 시리즈 덧셈')
seriessum = myseries01.add(myseries02, fill_value=10)
print(seriessum)

print('\n# 두 시리즈 뺄셈')
seriessub = myseries01.sub(myseries02, fill_value=30)
print(seriessub)