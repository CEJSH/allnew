def prime(num):
    if num == 2:
        return 1
    for i in range(2, num):
        if num % i == 0:
            return 0
            break
    return 1

