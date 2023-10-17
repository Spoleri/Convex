#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point, Interval
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    pass


def point_draw(self, tk):
    tk.draw_point(self.p)
    for i in self.li:
        tk.draw_line(i.p, i.q)


def segment_draw(self, tk):
    tk.draw_line(self.p, self.q)
    for i in self.li:
        tk.draw_line(i.p, i.q)


def polygon_draw(self, tk):
    for n in range(self.points.size()):
        tk.draw_line(self.points.last(), self.points.first())
        self.points.push_last(self.points.pop_first())
    for i in self.li:
        tk.draw_line(i.p, i.q)


setattr(Void, 'draw', void_draw)
setattr(Point, 'draw', point_draw)
setattr(Segment, 'draw', segment_draw)
setattr(Polygon, 'draw', polygon_draw)

print('Введите точки, образующие треугольник:')
a = R2Point()
t = True
while t:
    t = False
    b = R2Point()
    if b == a:
        print('Точка совпадает с предыдущей, попробуйте ещё раз.')
        t = True
t = True
while t:
    t = False
    c = R2Point()
    if R2Point.area(a, b, c) == 0:
        print('Точки не образуют треугольник, попробуйте ещё раз.')
        t = True
print('Ввод завершён')

li = (Interval(b, a), Interval(c, b), Interval(c, a))

tk = TkDrawer()
f = Void()
tk.clean()
f.draw(tk)

try:
    while True:
        if isinstance(f, Void):
            f = f.add(R2Point(), li)
        else:
            f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}, C = {f.count()}")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
