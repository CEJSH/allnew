import matplotlib
from pandas import Series
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

matplotlib.rcParams['axes.unicode_minus'] = False

mylist = [30, 20, 40, 60, 50]
myindex = ['이상화', '한용운', '노천명', '윤동주', '이육사']

print(myindex)
print(mylist)
print('-' * 50)

myseries = Series(data=mylist, index=myindex)
mylim = [0, myseries.max() + 10]
myseries.plot(title = '시험 점수', kind='line', ylim=mylim,
              grid=False, rot=0, use_index=True)

filename = 'seriesGraph02.png'

plt.savefig(filename, dpi=400, bbox_inches='tight')
print(filename + '파일이 저장되었습니다.')
plt.show()
