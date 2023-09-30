#!/usr/bin/env -S python3 -B
from tk_drawer import TkDrawer
from r2point import R2Point
from convex import Void, Point, Segment, Polygon


def void_draw(self, tk):
    for i in self.li:
        tk.draw_line(i.p, i.q)


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


tk = TkDrawer()
f = Void()
tk.clean()
f.draw(tk)

try:
    while True:
        f = f.add(R2Point())
        tk.clean()
        f.draw(tk)
        print(f"S = {f.area()}, P = {f.perimeter()}, C = {f.count()}")
except(EOFError, KeyboardInterrupt):
    print("\nStop")
    tk.close()
