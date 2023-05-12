class Rectangle(object):
    count = 0

    def __init__(self, width, height):
        self.width = width
        self.height = height
        Rectangle.count += 1

    def isSquare(recWidth, recHeight):
        return recWidth == recHeight

    def calcArea(self):
        return self.width * self.height

    def __add__(self,other):
        return Rectangle(self.width + other.width, self.height + other.height)

    def printCount(cls):
        print(cls.count)