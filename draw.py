from collections import namedtuple

Point = namedtuple('Point', ('x', 'y', 'z'))


def steep(a, b):
    return Point(a.y, a.x, a.z), Point(b.y, b.x, b.z)


def line(a, b, context, color):
    is_steep = False
    if abs(b.y - a.y) > abs(b.x - a.x):
        is_steep = True
        a, b = steep(a, b)
    if a.x > b.x:
        a, b = b, a

    dx, dy = abs(b.x - a.x), abs(b.y - a.y)

    error = 0
    derror = dy * 2
    direction = 1 if (b.y - a.y) > 0 else -1

    y = a.y

    for x in range(a.x, b.x):
        context[(x, y) if not is_steep else (y,x)] = color
        error += derror
        if error > dx:
            y += direction
            error -= dx * 2


def poly(a, b, c, context, color):
    line(a, b, context, color)
    line(b, c, context, color)
    line(c, a, context, color)