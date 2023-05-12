import urllib.request

url = 'https://shared-comic.pstatic.net/thumb/webtoon/648419/thumbnail/thumbnail_IMAG10_1421195d-13be-4cde-bcf9-0c78d51c5ea3.jpg'

savename = input('저장할 파일 이름 입력 : ')

result = urllib.request.urlopen(url)

data = result.read()
print('# type(data) :', type(data))

with open(savename, mode='wb') as f:
    f.write(data)
    print(savename + ' saved...')


### regular Expression

### 정규 표현식 플래그

# ^ : start string
# $ : end string
# * : 반복(all)
# + :  반복, 1번 이상
# ?  : 반복, 있거나 없거나
# {} : 반복 횟수
#
# [a-zA-Z] : 알파벳
# [0-9] : 숫자
# [^0-9] : 숫자가 아닌 것
# g : 전역 탐색
# i : 대소문자 구별하지 않음
# \d : 숫자
# \D : 숫자가 아닌 것
# \w :  문자, 숫자
# \W : 문자, 숫자 아닌 것
# \s : white space
# \S : white space 아닌 것
# Dot(.) : \n을 제외한 모든 문자
