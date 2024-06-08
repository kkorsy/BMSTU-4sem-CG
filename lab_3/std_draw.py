from tkinter import *
from math import radians, sin, cos
import time


def draw_axis(canvas, width, height):
    axis_space = 15
    canvas.create_line(0 + axis_space, 0 + axis_space, width - axis_space, 0 + axis_space, arrow=LAST)
    canvas.create_line(0 + axis_space, 0 + axis_space, 0 + axis_space, height - axis_space, arrow=LAST)

    canvas.create_text(10, 10, text='0')
    canvas.create_text(width - axis_space, axis_space + 5, text='x')
    canvas.create_text(axis_space + 7, height - axis_space, text='y')

    for x in range(100, width - axis_space, 100):
        canvas.create_line(x, axis_space - 5, x, axis_space + 5)
        canvas.create_text(x, axis_space + 10, text=str(x))

    for y in range(100, height - axis_space, 100):
        canvas.create_line(axis_space - 5, y, axis_space + 5, y)
        canvas.create_text(axis_space + 15, y, text=str(y))


def draw_standard_line(canvas, xn, yn, xk, yk, color, draw=True):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    if draw:
        canvas.create_line(xn, yn, xk, yk, fill=color)


def turn_point(xc, yc, xp, yp, alpha):
    x = xp
    px = xc + (x - xc) * cos(alpha) + (yp - yc) * sin(alpha)
    py = yc - (x - xc) * sin(alpha) + (yp - yc) * cos(alpha)

    return px, py


def draw_spector_by_alg(canvas, xc, yc, length, angle, color, alg, draw=True, intensive=False):
    steps = int(360 // angle)
    total = 0

    cur_x, cur_y = xc, yc - length
    for _ in range(steps):
        if intensive:
            t1 = time.time()
            t_temp = alg(canvas, xc, yc, round(cur_x), round(cur_y), color, intensive, draw=draw)
            t2 = time.time()
        else:
            t1 = time.time()
            alg(canvas, xc, yc, round(cur_x), round(cur_y), color, draw=draw)
            t2 = time.time()
        cur_x, cur_y = turn_point(xc, yc, cur_x, cur_y, radians(angle))
        total += t2 - t1

    return total / steps
