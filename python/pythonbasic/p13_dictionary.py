#!/usr/bin/env python
# key값은 중복될 수 없다.
me = {'name' : "Choi","Age":22,"gender":"female"}
print(me)

myname =me['name']
print(myname)

me['age'] = 25
print(me)

dict = {}
print(dict)

me[10] =10
print(me)

me['10'] =10
print(me)

me['job']='teacher'
print(me)

me['list'] = [1, 2, 3, 4, 5]

me[(1,2)] = 'this is value'
print(me)

me[3] = (3, 'aa', 5)
print(me)

print ("===============")
print(f'me[list] : {me["list"]}')
print(f'me[(1,2)] : {me[(1,2)]}')
print(f'me[3] : {me[3]}')

print(f'me[(1,2)] : {me[(1,2)]}')
me[(1,2)] = "This is real value"
print(f'me[(1,2)] : {me[(1,2)]}')

dic = {'a' : 1234, "b": "blog", "c":3333}

if 'b' in dic:
    print("b exists")
else:
    print("b does not exist")

if 'e' in dic:
    print("e exists")
else:
    print("e does not exist")

if 'blog' in dic.values():
    print('value exists')
else:
    print('value not exists')

print(dic.keys())

print(dic.values())

dic['d']=""
print(dic)

for k in dic.keys():
    print(f'key : {k}')
for v in dic.values():
    print(f'value : {v}')
# 리스트안에 튜플형태로
print(dic.items())
# 딕셔너리
print(dic)

for i in dic.items():
    print(f'all : {i}')
    print(f'key  : {i[0]}')
    print(f'value : {i[1]}')
    print()

v1 = dic.get('b')
print(f'dic.get["b"] : {v1}')

v2 = dic.get('z')
print(f"dic.get['z'] : {v2}")

# del

print(f'before : {dic}')

del dic['c']

print(f'after : {dic}')

# clear

dic.clear()
print(f'dic : {dic}')


