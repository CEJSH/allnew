import pandas as pd
import matplotlib.pyplot as plt
plt.rcParams['font.family'] = 'Malgun Gothic'

filename = 'ex802.csv'
myframe = pd.read_csv(filename, encoding='utf-8')
print(myframe)
myframe = myframe.set_index(keys='type')
print(myframe)

myframe.plot(kind='line', title='지역별 차종 교통량', figsize=(10, 6), legend=True)
filename = 'dataframeGraph02.png'
plt.savefig(filename, dpi=400, bbox_inches='tight')

print(filename + '파일이 저장되었습니다.')

plt.show()