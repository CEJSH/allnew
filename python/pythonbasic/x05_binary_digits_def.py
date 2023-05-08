import random
x = random.randint(4,16)
def binary_digits(x):
    binary =[]
    a = x

    while x > 0:
        binary.append(x % 2)
        x = x // 2
    binary.reverse()

    print(f'{a} binary number is {binary}')

binary_digits(x)



