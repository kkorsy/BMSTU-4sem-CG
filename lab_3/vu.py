import time
from math import floor
from brezenhem import get_rgb_intensity


def draw_vu(canvas, xn, yn, xk, yk, color, bg_color, draw=True, stepmode=False):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    I = 100
    t1 = time.time()
    gradient = get_rgb_intensity(canvas, color, bg_color, I)
    t2 = time.time()
    steep = abs(yk - yn) > abs(xk - xn)

    if steep:
        xn, yn = yn, xn
        xk, yk = yk, xk
    if xn > xk:
        xn, xk = xk, xn
        yn, yk = yk, yn

    dx = xk - xn
    dy = yk - yn

    if dx == 0:
        tg = 1
    else:
        tg = dy / dx

    x2 = round(xn)
    xpx1 = x2
    y = yn + tg * (x2 - xn) + tg

    xpx2 = int(xk + 0.5)

    steps = 0

    if steep:
        for x in range(xpx1, xpx2):
            if draw:
                try:
                    canvas.create_line(int(y), x, int(y) + 1, x, fill=gradient[int((I - 1) * (abs(1 - y + int(y))))])
                except:
                    canvas.create_line(int(y), x, int(y) + 1, x, fill=color)
                canvas.create_line(int(y) + 1, x, int(y) + 2, x, fill=gradient[int((I - 1) * (abs(y - int(y))))])

            if x < round(xk) and int(y) != int(y + tg):
                steps += 1

            y += tg
    else:
        for x in range(xpx1, xpx2):
            if draw:
                try:
                    canvas.create_line(x + 1, int(y), x + 2, int(y), fill=gradient[int((I - 1) * (abs(1 - y + int(y))))])
                except:
                    canvas.create_line(x + 1, int(y), x + 2, int(y), fill=color)
                canvas.create_line(x + 1, int(y) + 1, x + 2, int(y) + 1, fill=gradient[int((I - 1) * (abs(y - int(y))))])

            if x < round(xk) and int(y) != int(y + tg):
                steps += 1

            y += tg

    if stepmode:
        return steps
    return t2 - t1
