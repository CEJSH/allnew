a = int(input("Input First number : "))
b = int(input("Input Second number : "))
def gcd(a, b):
    if a > b:
        while b > 0:
            r = a % b
            a = b
            b = r
        return a
    else:
        while a > 0:
            r = b % a
            b = a
            a = r
        return b

print(gcd(a, b))
