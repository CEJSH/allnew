import random

data = random.sample(range(1,101),10)
print(data)
class findMax(object):

    def __init__(self, data):
        self.data = data
    def max(self):
        max = self.data[0]
        for i in data:
            if i > max:
                max = max

        return max

data1 = findMax(data)

print(f'Max value is : {data1.max()}')




