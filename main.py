from collections import namedtuple

from PIL import Image
from PIL import ImageColor as color
import math
from draw import line, poly

WIDTH = 1024
HEIGHT = 768

BG_COLOR = color.getrgb("#757575")
ORDINATES_COLOR = color.getrgb("#212121")
GRID_COLOR = color.getrgb("#616161")

Point = namedtuple('Point', ('x', 'y', 'z'))


def abre_line(points, pixel_data):
    _start, _end = points
    swap = False
    x0, y0 = _start
    x1, y1 = _end

    if abs(y1 - y0) > abs(x1 - x0):
        swap = True
        x0, y0 = y0, x0
        x1, y1 = y1, x1

    if x0 > x1:
        x0, x1 = x1, x0
        y0, y1 = y1, y0

    dx = x1 - x0
    dy = y1 - y0

    grad = dy / dx
    y = y0 + grad

    dp(pixel_data, swap, x0, y0, 1)
    dp(pixel_data, swap, x1, y1, 1)

    for x in range(x0 + 1, x1):
        dp(pixel_data, swap, x, y, 1 - (y - int(y)))
        dp(pixel_data, swap, x, y + 1, y - int(y))
        y += grad


def dp(pd, swap, x, y, hue):
    gradient_percent = int(hue * 100 / 1)
    gradient_color = "#f2f2f2"

    if gradient_percent < 20:
        gradient_color = '#a6a6a6'
    elif 20 < gradient_percent < 40:
        gradient_color = '#bfbfbf'
    elif 40 < gradient_percent < 60:
        gradient_color = '#d9d9d9'
    elif 60 < gradient_percent < 80:
        gradient_color = '#e6e6e6'
    else:
        gradient_color = "#f2f2f2"

    if not swap:
        pd[(x, int(y))] = color.getrgb(gradient_color)
    else:
        pd[(y, int(x))] = color.getrgb(gradient_color)


def bre_line(points, pixel_data, color):
    steep = False
    x0, y0 = points[0]
    x1, y1 = points[1]

    if abs(y1 - y0) > abs(x1 - x0):
        steep = True
        x0, y0, x1, y1 = y0, x0, y1, x1

    if x0 > x1:
        x0, x1, y0, y1 = x1, x0, y1, y0

    dx, dy = abs(x1 - x0), abs(y1 - y0)

    error = 0
    derr2 = dy * 2

    direction = 1 if (y1 - y0) > 0 else -1
    y = y0

    for x in range(x0, x1):
        pixel_data[(x, y) if not steep else (y, x)] = color
        error += derr2
        if error > dx:
            y += direction
            error -= dx * 2


def dda_line(points, pixel_data):
    _start, _end = points

    x0, y0 = _start
    x1, y1 = _end

    dx = abs(x1 - x0)
    dy = abs(y1 - y0)

    l = max((dx, dy))

    dx = (x1 - x0) / l
    dy = (y1 - y0) / l

    x, y = x0 + 0.5, y0 + 0.5

    for step in range(l + 1):
        pixel_data[(math.floor(x), math.floor(y))] = color.getrgb("#fff")
        x = x + dx
        y = y + dy


def normalize_cords(xy):
    zero_point = (WIDTH // 2, HEIGHT // 2)

    def _check_point(xy):
        x, y = xy
        if not (0 <= x < WIDTH and 0 <= y < HEIGHT):
            raise ValueError('pixel location out of range')

    x, y = xy

    x += zero_point[0]
    y = zero_point[1] - y

    _check_point((x, y))

    return x, y


def draw_ordinates(pixel_data, pic):
    x_center = pic.width // 2
    y_center = pic.height // 2

    for x in range(0, pic.width, 10):
        for y in range(pic.height):
            pixel_data[x, y] = GRID_COLOR

    for y in range(0, pic.height, 10):
        for x in range(pic.width):
            pixel_data[x, y] = GRID_COLOR

    for x_cord in range(pic.width):
        pixel_data[x_cord, y_center] = ORDINATES_COLOR
        if (x_cord % 10) == 0:
            for y in range(y_center - 3, y_center + 3):
                pixel_data[x_cord, y] = ORDINATES_COLOR

    for y_cord in range(pic.height):
        pixel_data[x_center, y_cord] = ORDINATES_COLOR
        if (y_cord % 10) == 0:
            for x in range(x_center - 3, x_center + 3):
                pixel_data[x, y_cord] = ORDINATES_COLOR


def get_obj():
    vertexes = []
    faces = []

    def get_faces(face):
        return tuple(int(f) for f in face.strip('\n').split('/'))

    with open('head.obj', 'r') as head:
        for i in head:
            row = i.split(' ')
            if row[0] == 'v':
                vertexes.append(Point(*(float(vertex) for vertex in row[1:])))
            if row[0] == 'f':
                faces.append([get_faces(face) for face in row[1:]])
    return vertexes, faces


def main():
    pic = Image.new('RGB', (WIDTH, HEIGHT), BG_COLOR)
    print('main mother fucker ga')

    vertex, faces = get_obj()
    data = pic.load()
    draw_ordinates(data, pic)
    line_color = color.getrgb("#fff")

    def normalize_cords(point):
        x = int((point.x + 1) * (WIDTH - 1) / 2)
        y = int((point.y + 1) * (HEIGHT - 1) / 2)
        return Point(x, y, point.z)

    # for face in faces:
    #     A, B, C = tuple(normalize_cords(vertex[f[0] - 1]) for f in face)
    #     poly(A, B, C, data, line_color)

    a = (Point(10, 70, 0), Point(50,160, 0), Point(70, 80, 0))
    # b = (Point(180, 50, 0), Point(150, 1, 0), Point(70, 180, 0))
    # c = (Point(180, 150, 0), Point(120, 160, 0), Point(130, 180, 0))

    a = tuple(sorted(a, key=lambda x: x.y))
    # b = tuple(sorted(b, key=lambda x: x.y))
    # c = tuple(sorted(c, key=lambda x: x.y))


    height = a[2].y - a[0].y

    y = a[0].y

    

    line(a[0], a[1], data, color.getrgb("#0f0"))
    line(a[1], a[2], data, color.getrgb("#0f0"))
    line(a[2], a[0], data, color.getrgb("#f00"))

    # line(b[0], b[1], data, color.getrgb("#0f0"))
    # line(b[1], b[2], data, color.getrgb("#0f0"))
    # line(b[2], b[0], data, color.getrgb("#f00"))
    #
    # line(c[0], c[1], data, color.getrgb("#0f0"))
    # line(c[1], c[2], data, color.getrgb("#0f0"))
    # line(c[2], c[0], data, color.getrgb("#f00"))

    # poly(*a, data, color.getrgb("#f00"))
    # poly(*b, data, color.getrgb("#0f0"))
    # poly(*c, data, color.getrgb("#00f"))

    pic.show()


if __name__ == '__main__':
    main()
