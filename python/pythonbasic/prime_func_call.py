import prime_func

a = int(input("please input number :"))

if prime_func.prime(a) == 0:
    print("%d 는 prime number가 아닙니다." % a)
else:
    print("%d 는 prime number입니다." % a)