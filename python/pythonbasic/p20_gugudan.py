while True:
    n = input("input number (q : quit) :")
    if n == 'q':
        break
    n = int(n)
    if n==1 or n>9:
        print('input number range 2~9')
    else:
        for i in range(1,10):
            print(f'{n}X{i}={n*i}')

