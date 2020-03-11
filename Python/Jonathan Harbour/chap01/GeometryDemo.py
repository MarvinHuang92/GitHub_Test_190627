# OOP Geometry Demo

class Point():
    x = 0.0
    y = 0.0

    def __init__(self, x, y):
        self.x = x
        self.y = y
        print("Point constructor")

    def ToString(self):
        return "{X:" + str(self.x) + ",Y:" + str(self.y) + "}"

class Size():
    width = 0.0
    height = 0.0

    def __init__(self,width,height):
        self.width = width
        self.height = height
        print("Size constructor")

    def ToString(self):
        return "{WIDTH=" + str(self.width) + \
               ",HEIGHT=" + str(self.height) + "}"

class Circle(Point):
    radius = 0.0

    def __init__(self, x, y, radius):
        super().__init__(x,y)
        self.radius = radius
        print("Circle constructor")

    def ToString(self):
        return super().ToString() + \
               ",{RADIUS=" + str(self.radius) + "}"

    def CalcCirum(self):
        return "Circumference = " + str(2 * 3.14159 * self.radius)

class Ellipse(Point,Size):
    def __init__(self, x, y, width, height):
        Point.__init__(self,x,y)
        Size.__init__(self,width,height)
        print("Ellipse constructor")

    def ToString(self):
        return Point.ToString(self) + \
               ",{A=" + str(self.width) + \
               ",B=" + str(self.height) + "}"


class Rectangle(Point,Size):
    def __init__(self, x, y, width, height):
        Point.__init__(self,x,y)
        Size.__init__(self,width,height)
        print("Rectangle constructor")

    def ToString(self):
        return Point.ToString(self) + "," + Size.ToString(self)

    def CalcArea(self):
        return "Area = " + str(self.width * self.height)
        

p = Point(10,20)
print(p.ToString())
print()

s = Size(80,70)
print(s.ToString())
print()

c = Circle(100,100,50)
print(c.ToString())
print(c.CalcCirum())
print()

r = Rectangle(200,250,40,50)
print(r.ToString())
print(r.CalcArea())
print()

e = Ellipse(300,350,60,70)
print(e.ToString())
print()