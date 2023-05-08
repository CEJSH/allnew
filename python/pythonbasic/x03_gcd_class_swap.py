a = int(input("Input First number : "))
b = int(input("Input Second number : "))

class Gcd(object):
    def __init__(self,a ,b):
        self.a = a
        self.b = b
    def gcd(self):
        if self.a < self.b:
            self.a, self.b = self.b, self.a
            print(f"gcd ({self.a}, {self.b})")
        while self.b > 0:
            r = self.a % self.b
            print(f"gcd ({self.b}, {r})")
            self.a = self.b
            self.b = r
        return self.a

print(f"gcd ({a}, {b}) of {a}, {b} : {Gcd(a, b).gcd()}")