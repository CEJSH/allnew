import random
x = random.randint(4,16)

class binary_digits(object):
    def __init__(self, x):
        self.x = x

    def convert(self):
        binary =[]

        while self.x > 0:
            binary.append(self.x % 2)
            self.x = self.x // 2
        binary.reverse()
        print(f'{x} binary number is {binary}')

Binary_digits = binary_digits(x)
Binary_digits.convert()



