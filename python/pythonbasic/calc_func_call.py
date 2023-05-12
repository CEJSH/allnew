import calc_func

a = int(input("please input first number : "))
b = int(input("please input second number : "))


print('{} + {} = {}'.format(a, b, calc_func.add(a, b)))
print('{} + {} = {}'.format(a, b, calc_func.sub(a, b)))

