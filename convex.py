from coverage import Coverage
from deq import Deq
from r2point import R2Point, Interval


class Figure:
    """ Абстрактная фигура """

    def perimeter(self):
        return 0.0

    def area(self):
        return 0.0

    def count(self):
        return 0


class Void(Figure):
    """ "Hульугольник" """

    def add(self, p, li):
        return Point(p, li)


class Point(Figure):
    """ "Одноугольник" """

    def __init__(self, p, li):
        self.li = li
        self.p = p

    def add(self, q):
        return self if self.p == q else Segment(self.p, q, self.li)


class Segment(Figure):
    """ "Двуугольник" """

    def __init__(self, p, q, li):
        self.li = li
        self.p, self.q = p, q
        val = Interval(p, q)
        self.cast = 0
        if all(not val.intersection(t) for t in self.li) and all(
                val.out_of_ambit(c) >= 1 for c in li) and not (
                (p + q) * 0.5).in_triangle(li):
            self.cast += 2

    def perimeter(self):
        return 2.0 * self.p.dist(self.q)

    def count(self):
        return self.cast

    def add(self, r):
        if R2Point.is_triangle(self.p, self.q, r):
            return Polygon(self.p, self.q, r, self.li)
        elif self.q.is_inside(self.p, r):
            return Segment(self.p, r, self.li)
        elif self.p.is_inside(r, self.q):
            return Segment(r, self.q, self.li)
        else:
            return self


class Polygon(Figure):
    """ Многоугольник """

    def __init__(self, a, b, c, li):
        self.li = li
        self.points = Deq()
        self.points.push_first(b)
        if b.is_light(a, c):
            self.points.push_first(a)
            self.points.push_last(c)
        else:
            self.points.push_last(a)
            self.points.push_first(c)
        self._perimeter = a.dist(b) + b.dist(c) + c.dist(a)
        self._area = abs(R2Point.area(a, b, c))
        self.cast = 0
        val_list = (Interval(a, b), Interval(c, a), Interval(b, c))
        for i in val_list:
            if all(not i.intersection(t) and i.out_of_ambit(t) >= 1
                    for t in self.li) and not ((i.p + i.q) * 0.5).in_triangle(
                    li):
                self.cast += 1

    def perimeter(self):
        return self._perimeter

    def area(self):
        return self._area

    def count(self):
        return self.cast

    # добавление новой точки
    def add(self, t):

        # поиск освещённого ребра
        for n in range(self.points.size()):
            if t.is_light(self.points.last(), self.points.first()):
                break
            self.points.push_last(self.points.pop_first())

        # хотя бы одно освещённое ребро есть
        if t.is_light(self.points.last(), self.points.first()):

            # учёт удаления ребра, соединяющего конец и начало дека
            self._perimeter -= self.points.first().dist(self.points.last())
            self._area += abs(R2Point.area(t,
                                           self.points.last(),
                                           self.points.first()))

            # удаление освещённых рёбер из начала дека
            p = self.points.pop_first()
            a = p
            while t.is_light(p, self.points.first()):
                self._perimeter -= p.dist(self.points.first())
                self._area += abs(R2Point.area(t, p, self.points.first()))

                i = Interval(self.points.first(), p)
                # Удаляемый отрезок удовлетворял условию? да => удаляем
                if all(not i.intersection(e) and i.out_of_ambit(e) >= 1 for
                        e in self.li) and not (
                        (self.points.first() + p) * 0.5).in_triangle(self.li):
                    self.cast -= 1

                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()

            i = Interval(a, p)
            # Учет промежуточного отрезка
            if all(not i.intersection(e) and i.out_of_ambit(e) >= 1
                   for e in self.li) and not (
                    (a + p) * 0.5).in_triangle(self.li):
                self.cast -= 1

            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))

                i = Interval(self.points.last(), p)
                # Удаляемый отрезок удовлетворял условию? да => удаляем
                if all(not i.intersection(e) and i.out_of_ambit(e) >= 1 for
                       e in self.li) and not (
                        (self.points.last() + p) * 0.5).in_triangle(self.li):
                    self.cast -= 1

                p = self.points.pop_last()

            self.points.push_last(p)
            i = Interval(t, self.points.last())
            if all(not i.intersection(e) and i.out_of_ambit(e) >= 1 for
                   e in self.li) and not (
                    (t + self.points.last()) * 0.5).in_triangle(self.li):
                self.cast += 1

            i = Interval(t, self.points.first())
            if all(not i.intersection(e) and i.out_of_ambit(e) >= 1 for
                   e in self.li) and not (
                    (t + self.points.first()) * 0.5).in_triangle(self.li):
                self.cast += 1

            # добавление двух новых рёбер
            self._perimeter += t.dist(self.points.first()) + \
                t.dist(self.points.last())
            self.points.push_first(t)

        return self


if __name__ == "__main__":
    f = Void()
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(1.0, 0.0))
    print(type(f), f.__dict__)
    f = f.add(R2Point(0.0, 1.0))
    print(type(f), f.__dict__)
