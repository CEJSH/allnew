import os

myfile01 = open('sample02.txt','rt', encoding='UTF-8')
linelists = myfile01.readlines()
myfile01.close()

myfile02 = open('result02.txt','wt',encoding='UTF-8')
final_lists = []
for i in linelists:
    info = i.strip('\n').split(" ")
    if int(info[1]) >=19:
        text = ('{}/{}/성년'.format(info[0],info[1]))
    else:
        text = ('{}/{}/미성년'.format(info[0], info[1]))
    myfile02.write(text + '\n')
myfile02.close()

myfile03 = open('result02.txt','rt', encoding='UTF-8')
line = 1
while line:
    line = myfile03.readline()
    print(line)
myfile03.close()
