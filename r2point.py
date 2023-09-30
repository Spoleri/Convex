from math import sqrt
from sympy.abc import t, T
from sympy import linsolve


class R2Point:
    """ Точка (Point) на плоскости (R2) """

    # Конструктор
    def __init__(self, x=None, y=None):
        if x is None:
            x = float(input("x -> "))
        if y is None:
            y = float(input("y -> "))
        self.x, self.y = x, y

    # Площадь треугольника
    @staticmethod
    def area(a, b, c):
        return 0.5 * ((a.x - c.x) * (b.y - c.y) - (a.y - c.y) * (b.x - c.x))

    # Лежат ли точки на одной прямой?
    @staticmethod
    def is_triangle(a, b, c):
        return R2Point.area(a, b, c) != 0.0

    # Расстояние до другой точки
    def dist(self, other):
        return sqrt((other.x - self.x)**2 + (other.y - self.y)**2)

    # Лежит ли точка внутри "стандартного" прямоугольника?
    def is_inside(self, a, b):
        return (((a.x <= self.x and self.x <= b.x) or
                 (a.x >= self.x and self.x >= b.x)) and
                ((a.y <= self.y and self.y <= b.y) or
                 (a.y >= self.y and self.y >= b.y)))

    # Освещено ли из данной точки ребро (a,b)?
    def is_light(self, a, b):
        s = R2Point.area(a, b, self)
        return s < 0.0 or (s == 0.0 and not self.is_inside(a, b))

    # Совпадает ли точка с другой?
    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.x == other.x and self.y == other.y
        return False


class Interval:

    def __init__(self, u, v):
        self.p, self.q = u, v
        self.kx = self.q.x - self.p.x
        self.ky = self.q.y - self.p.y
        self.x = self.kx * t + self.p.x
        self.y = self.ky * t + self.p.y

    def intersection(self, other):
        if self.kx == other.kx == 0 or self.ky == other.ky == 0:
            return False
        if not (self.kx == 0 or other.kx == 0 or self.ky == 0 or
                other.ky == 0) and self.kx / other.kx == self.ky / other.ky:
            return False
        x = other.x.subs(t, T)
        y = other.y.subs(t, T)
        a = tuple(linsolve([self.x - x, self.y - y], (t, T)))[0]
        if 0 < a[0] < 1 and 0 < a[1] < 1:
            return True
        else:
            return False


if __name__ == "__main__":
    x = R2Point(1.0, 1.0)
    print(type(x), x.__dict__)
    print(x.dist(R2Point(1.0, 0.0)))
    a, b, c = R2Point(0.0, 0.0), R2Point(1.0, 0.0), R2Point(1.0, 1.0)
    print(R2Point.area(a, c, b))
