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

    def __init__(self, p_1=None, p_2=None, p_3=None):
        if p_1 is None or p_2 is None or p_3 is None:
            print("Впишите координаты 3 точек, задающих треугольник:")
            p_1 = R2Point()
            t = True
            while t or p_1 == p_2:
                t = False
                p_2 = R2Point()
                if p_2 == p_1:
                    print('Введённая точка совпадает с введенной ранее, '
                          'попробуйте ещё раз')
            line_1 = Interval(p_1, p_2)
            t = True
            while t:
                t = False
                p_3 = R2Point()
                if p_3 == p_1 or p_3 == p_2:
                    t = True
                    print('Введённая точка совпадает с введенной ранее, '
                          'попробуйте ещё раз:')
                    continue
                line_2 = Interval(p_1, p_3)
                if line_1.kx == line_2.kx == 0 or line_1.ky == line_2.ky == 0:
                    t = True
                    continue

                if not (line_1.kx == 0 or line_2.kx == 0 or line_1.ky == 0 or
                        line_2.ky == 0) \
                        and line_1.kx / line_2.kx == line_1.ky / line_2.ky:
                    t = True
                    print('Введенные точки лежат на одной прямой, попробуйте '
                          'ещё'
                          'раз:')
            print("Ввод закончен")
        line_1 = Interval(p_2, p_1)
        line_2 = Interval(p_3, p_2)
        line_3 = Interval(p_1, p_3)
        self.li = [line_1, line_2, line_3]

    def add(self, p):
        return Point(p, self.li)


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
        if all(not val.intersection(t) for t in self.li):
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
            if all(not i.intersection(t) for t in self.li) and not (
                    i.q.in_triangle(self.li) or i.p.in_triangle(self.li)):
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

                # Удаляемый отрезок удовлетворял условию? да => удаляем
                if all(not Interval(self.points.first(), p).intersection(e)
                       for e in self.li) and not (p.in_triangle(self.li) or
                        self.points.first().in_triangle(self.li)):
                    self.cast -= 1

                p = self.points.pop_first()
            self.points.push_first(p)

            # удаление освещённых рёбер из конца дека
            p = self.points.pop_last()

            # Учет промежуточного отрезка
            if all(not Interval(a, p).intersection(e) for e in self.li) \
                    and not (p.in_triangle(self.li) or a.in_triangle(self.li)):
                self.cast -= 1

            while t.is_light(self.points.last(), p):
                self._perimeter -= p.dist(self.points.last())
                self._area += abs(R2Point.area(t, p, self.points.last()))

                # Удаляемый отрезок удовлетворял условию? да => удаляем
                if all(not Interval(self.points.last(), p).intersection(e)
                       for e in self.li) and not (p.in_triangle(self.li) or
                self.points.last().in_triangle(self.li)):
                    self.cast -= 1

                p = self.points.pop_last()
            self.points.push_last(p)

            if all(not Interval(t, self.points.last()).intersection(e) for
                   e in self.li) and not (
                    t.in_triangle(self.li) or self.points.last().in_triangle(
                    self.li)):
                self.cast += 1

            if all(not Interval(t, self.points.first()).intersection(e) for
                   e in self.li) and not (
                    t.in_triangle(self.li) or self.points.first().in_triangle(
                    self.li)):
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
