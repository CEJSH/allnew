import x01
def findMax(data):
    max = data[0]
    for i in data:
        if max > i:
            max = max
        else:
            max = i
    return max

print(findMax(x01.data))



