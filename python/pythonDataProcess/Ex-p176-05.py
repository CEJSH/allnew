import numpy as np
from pandas import Series, DataFrame

myindex = ['윤봉길', '김유신','신사임당']
mylist = [30, 40, 50]

myseries = Series(data=mylist, index=myindex)
print('\n시리즈의 결과 출력')
print(myseries)

myindex2=['윤봉길','김유신','이순신']
mylist = list(i * 3 for i in range(1,10))
mycol = ['용산구', '마포구', '서대문구']
myframe = DataFrame(np.reshape(np.array(mylist), (3,3)),
                    index=myindex2, columns=mycol)
print('\n데이터프레임 출력')
print(myframe)

myindex3 = ['윤봉길', '김유신','이완용']
mycol2 = ['용산구', '마포구', '은평구']
mylist2 = list(i * 5 for i in range(1,10))
myframe2 = DataFrame(np.reshape(np.array(mylist2), (3,3)),
                    index=myindex3, columns=mycol2)
print('\n데이터프레임 출력')
print(myframe2)



print('\nmyframe + myseries')
result = myframe.add(myseries, axis = 0)
print(result)

print('\nDataframe + Dataframe')
result = myframe.add(myframe2, fill_value = 20)
print(result)

print('\nDataframe - Dataframe')
result = myframe.sub(myframe2, fill_value = 10)
print(result)