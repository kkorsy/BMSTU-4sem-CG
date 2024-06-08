from tkinter import *
from math import *
from point_class import *
import numpy as np
import matplotlib
from matplotlib.patches import Polygon
from matplotlib.axis import Axis
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter.messagebox import *

matplotlib.use('TkAgg')

# создание окна
wind = Tk()
wind.state('zoomed')
wind.title('Lab 2')


# создание кнопки
def create_button(frame, btn_name, row, column, columnspan, cmd):
    btn = Button(frame, text=btn_name, command=cmd, font="Consolas 14", bg="#fffafa")
    btn.grid(row=row, column=column, columnspan=columnspan, padx=1, pady=1, sticky=NSEW)

    return btn


# создание поля ввода
def create_entry(frame, row, column, columnspan):
    ent = Entry(frame, font="Consolas 14", width=10)
    ent.grid(row=row, column=column, columnspan=columnspan, padx=1, pady=1, sticky=NSEW)

    return ent


# создание надписи
def create_label(frame, text, row, column, columnspan):
    lb = Label(frame, text=text, font="Consolas 14")
    lb.grid(row=row, column=column, columnspan=columnspan, padx=1, pady=1, sticky=NSEW)

    return lb


def create_frame(row, column, rowspan, columnspan):
    frm = Frame(wind, bg='darkgrey')
    for i in range(4):
        frm.columnconfigure(index=i, weight=1)
    frm.grid(row=row, column=column, rowspan=rowspan, columnspan=columnspan, padx=10, pady=10, sticky=NSEW)

    return frm


def info_transfer():
    showinfo("Перенос", "dx - смещение вдоль оси Х\ndy - смещение вдоль оси Y")


def info_turn():
    showinfo("Поворот", "xc - координата х центра поворота\nyc - координата y центра поворота\n"
                        "Угол - величина поворота в градусах")


def info_scale():
    showinfo("Масштабирование", "xc - координата х центра масштабирования\nyc - координата y центра масштабирования\n"
                                "kx, ky - коэффициенты масштабирования")


def fill_frame(frm, frm_name, info):
    if frm == frame_back:
        create_label(frm, "Шаг назад", 0, 0, 2)
        create_label(frm, "Шаг вперед", 0, 2, 2)
        back = create_button(frm, "<----", 1, 0, 2, back_step)
        forward = create_button(frm, "---->", 1, 2, 2, forward_step)
        return back, forward

    create_label(frm, frm_name, 0, 0, 3)
    create_button(frm, "i", 0, 3, 1, info)
    if frm == frame_transfer:
        create_label(frm, "dx", 1, 0, 2)
        create_label(frm, "dy", 1, 2, 2)
        dx = create_entry(frm, 2, 0, 2)
        dy = create_entry(frm, 2, 2, 2)
        trans = create_button(frm, "Переместить", 3, 0, 4, transfer)
        return dx, dy, trans
    elif frm == frame_turn:
        create_label(frm, "xc", 1, 0, 1)
        create_label(frm, "yc", 1, 1, 1)
        create_label(frm, "угол", 1, 2, 2)
        xc = create_entry(frm, 2, 0, 1)
        yc = create_entry(frm, 2, 1, 1)
        angle = create_entry(frm, 2, 2, 2)
        t = create_button(frame_turn, "Повернуть", 3, 0, 4, turn)
        return xc, yc, angle, t
    elif frm == frame_scaling:
        create_label(frm, "xc", 1, 0, 1)
        create_label(frm, "yc", 1, 1, 1)
        create_label(frm, "kx", 1, 2, 1)
        create_label(frm, "ky", 1, 3, 1)
        xc = create_entry(frm, 2, 0, 1)
        yc = create_entry(frm, 2, 1, 1)
        kx = create_entry(frm, 2, 2, 1)
        ky = create_entry(frm, 2, 3, 1)
        s = create_button(frm, "Масштабировать", 3, 0, 4, scale)
        return xc, yc, kx, ky, s


def draw_figure():
    def f1(x):
        return exp(x)

    def f2(x):
        return exp(-x)

    def f3(x):
        return x ** 2

    g_1, g_2, g_3 = [], [], []
    i, step = X_MIN, 1 / 100
    while i <= X_MAX:
        g_1.append(Point(i, f1(i)))
        g_2.append(Point(i, f2(i)))
        g_3.append(Point(i, f3(i)))
        i += step

    plot.plot(list(i.x for i in g_1), list(i.y for i in g_1))
    plot.plot(list(i.x for i in g_2), list(i.y for i in g_2))
    plot.plot(list(i.x for i in g_3), list(i.y for i in g_3))

    return g_1, g_2, g_3


def stroke():
    global pl

    p = Polygon(pl, fill=False, closed=True, hatch='////')
    plot.add_patch(p)


def find_cross(g_1, g_2):
    g_1, g_2 = sorted(g_1), sorted(g_2)
    min_diff = 1000
    res = (None, None)
    for i in range(len(g_1)):
        if abs(g_1[i].y - g_2[i].y) < min_diff:
            res = (g_1[i].x, g_1[i].y)
            min_diff = abs(g_1[i].y - g_2[i].y)
    return res


def clear():
    global canvas
    plot.clear()
    plot.axvline(0, color='grey')
    plot.axhline(0, color='grey')
    Axis.set(plot, xlim=(X_MIN, X_MAX), ylim=(Y_MIN, Y_MAX))
    plot.plot(1, 0, ls="", marker=">", ms=5, color="grey", transform=plot.get_yaxis_transform(), clip_on=False)
    plot.plot(0, 1, ls="", marker="^", ms=5, color="grey", transform=plot.get_xaxis_transform(), clip_on=False)
    plot.grid(True, which='major', linewidth=1)
    plot.grid(True, which='minor', linewidth=1)
    canvas = FigureCanvasTkAgg(figure, wind)
    canvas.get_tk_widget().place(x=460, y=-100)


def redraw():
    global graph_1, graph_2, graph_3, cr
    clear()
    plot.plot(list(i.x for i in graph_1), list(i.y for i in graph_1))
    plot.plot(list(i.x for i in graph_2), list(i.y for i in graph_2))
    plot.plot(list(i.x for i in graph_3), list(i.y for i in graph_3))
    plot.scatter(cr.one.x, cr.one.y, s=20, color='red', zorder=5)
    plot.scatter(cr.two.x, cr.two.y, s=20, color='red', zorder=5)
    plot.scatter(cr.three.x, cr.three.y, s=20, color='red', zorder=5)
    stroke()


def get_transfer_matrix(dx, dy):
    matrix = np.identity(3)
    matrix[2][0], matrix[2][1] = dx, dy
    return matrix


def mult_transfer(coords, dx, dy):
    matrix = get_transfer_matrix(dx, dy)
    xt, yt, t = np.dot(coords, matrix)
    return xt, yt


def cr_transfer(dx, dy):
    global cr, pl
    for i in range(len(pl)):
        pl[i][0], pl[i][1] = mult_transfer((pl[i][0], pl[i][1], 1), dx, dy)
    cr.one.x, cr.one.y = mult_transfer((cr.one.x, cr.one.y, 1), dx, dy)
    cr.two.x, cr.two.y = mult_transfer((cr.two.x, cr.two.y, 1), dx, dy)
    cr.three.x, cr.three.y = mult_transfer((cr.three.x, cr.three.y, 1), dx, dy)


def transfer():
    global graph_1, graph_2, graph_3, history
    try:
        dx, dy = float(ent_dx.get()), float(ent_dy.get())
    except ValueError:
        showerror("Ошибка", "Введены некорректные данные")
    else:
        for i in range(len(graph_1)):
            graph_1[i].x, graph_1[i].y = mult_transfer((graph_1[i].x, graph_1[i].y, 1), dx, dy)
            graph_2[i].x, graph_2[i].y = mult_transfer((graph_2[i].x, graph_2[i].y, 1), dx, dy)
            graph_3[i].x, graph_3[i].y = mult_transfer((graph_3[i].x, graph_3[i].y, 1), dx, dy)
        history.append_new(get_inv_transfer(dx, dy))
        cr_transfer(dx, dy)
        redraw()


def get_inv_transfer(dx, dy):
    matrix_transfer = get_transfer_matrix(dx, dy)
    return np.linalg.inv(matrix_transfer)


def get_scale_matrix(kx, ky):
    matrix = np.identity(3)
    matrix[0][0], matrix[1][1] = kx, ky
    return matrix


def mult_scale(coords, kx, ky):
    matrix = get_scale_matrix(kx, ky)
    xt, yt, t = np.dot(coords, matrix)
    return xt, yt


def cr_scale(xc, yc, kx, ky):
    global cr, pl
    for i in range(len(pl)):
        xt, yt = mult_transfer((pl[i][0], pl[i][1], 1), -xc, -yc)
        xt, yt = mult_scale((xt, yt, 1), kx, ky)
        pl[i][0], pl[i][1] = mult_transfer((xt, yt, 1), xc, yc)

    cr.one.x, cr.one.y = mult_transfer((cr.one.x, cr.one.y, 1), -xc, -yc)
    cr.one.x, cr.one.y = mult_scale((cr.one.x, cr.one.y, 1), kx, ky)
    cr.one.x, cr.one.y = mult_transfer((cr.one.x, cr.one.y, 1), xc, yc)

    cr.two.x, cr.two.y = mult_transfer((cr.two.x, cr.two.y, 1), -xc, -yc)
    cr.two.x, cr.two.y = mult_scale((cr.two.x, cr.two.y, 1), kx, ky)
    cr.two.x, cr.two.y = mult_transfer((cr.two.x, cr.two.y, 1), xc, yc)

    cr.three.x, cr.three.y = mult_transfer((cr.three.x, cr.three.y, 1), -xc, -yc)
    cr.three.x, cr.three.y = mult_scale((cr.three.x, cr.three.y, 1), kx, ky)
    cr.three.x, cr.three.y = mult_transfer((cr.three.x, cr.three.y, 1), xc, yc)


def scale():
    global graph_1, graph_2, graph_3
    try:
        kx, ky = float(ent_kx.get()), float(ent_ky.get())
        xc, yc = float(ent_xc_scale.get()), float(ent_yc_scale.get())
    except ValueError:
        showerror("Ошибка", "Введены некорректные данные")
    else:
        if kx == 0 or ky == 0:
            showerror("Ошибка", "Коэффициент масштабирования не может быть равен нулю")
            return

        for i in range(len(graph_1)):
            xt, yt = mult_transfer((graph_1[i].x, graph_1[i].y, 1), -xc, -yc)
            xt, yt = mult_scale((xt, yt, 1), kx, ky)
            graph_1[i].x, graph_1[i].y = mult_transfer((xt, yt, 1), xc, yc)

            xt, yt = mult_transfer((graph_2[i].x, graph_2[i].y, 1), -xc, -yc)
            xt, yt = mult_scale((xt, yt, 1), kx, ky)
            graph_2[i].x, graph_2[i].y = mult_transfer((xt, yt, 1), xc, yc)

            xt, yt = mult_transfer((graph_3[i].x, graph_3[i].y, 1), -xc, -yc)
            xt, yt = mult_scale((xt, yt, 1), kx, ky)
            graph_3[i].x, graph_3[i].y = mult_transfer((xt, yt, 1), xc, yc)
        history.append_new(get_inv_scale(xc, yc, kx, ky))
        cr_scale(xc, yc, kx, ky)
        redraw()


def get_inv_scale(xc, yc, kx, ky):
    matrix_transfer1 = get_transfer_matrix(-xc, -yc)
    matrix_scale = get_scale_matrix(kx, ky)
    matrix_transfer2 = get_transfer_matrix(xc, yc)

    m = np.dot(np.dot(matrix_transfer1, matrix_scale), matrix_transfer2)
    return np.linalg.inv(m)


def get_turn_matrix(phi):
    matrix = np.identity(3)
    matrix[0][0], matrix[0][1], matrix[1][0], matrix[1][1] = cos(phi), -sin(phi), sin(phi), cos(phi)
    return matrix


def mult_turn(coords, phi):
    matrix = get_turn_matrix(phi)
    xt, yt, t = np.dot(coords, matrix)
    return xt, yt


def cr_turn(xc, yc, phi):
    global cr, pl
    for i in range(len(pl)):
        xt, yt = mult_transfer((pl[i][0], pl[i][1], 1), -xc, -yc)
        xt, yt = mult_turn((xt, yt, 1), phi)
        pl[i][0], pl[i][1] = mult_transfer((xt, yt, 1), xc, yc)

    cr.one.x, cr.one.y = mult_transfer((cr.one.x, cr.one.y, 1), -xc, -yc)
    cr.one.x, cr.one.y = mult_turn((cr.one.x, cr.one.y, 1), phi)
    cr.one.x, cr.one.y = mult_transfer((cr.one.x, cr.one.y, 1), xc, yc)

    cr.two.x, cr.two.y = mult_transfer((cr.two.x, cr.two.y, 1), -xc, -yc)
    cr.two.x, cr.two.y = mult_turn((cr.two.x, cr.two.y, 1), phi)
    cr.two.x, cr.two.y = mult_transfer((cr.two.x, cr.two.y, 1), xc, yc)

    cr.three.x, cr.three.y = mult_transfer((cr.three.x, cr.three.y, 1), -xc, -yc)
    cr.three.x, cr.three.y = mult_turn((cr.three.x, cr.three.y, 1), phi)
    cr.three.x, cr.three.y = mult_transfer((cr.three.x, cr.three.y, 1), xc, yc)


def turn():
    global graph_1, graph_2, graph_3, history
    try:
        phi = float(ent_angle.get())
        xc, yc = float(ent_xc_turn.get()), float(ent_yc_turn.get())
    except ValueError:
        showerror("Ошибка", "Введены некорректные данные")
    else:
        phi = radians(phi)
        for i in range(len(graph_1)):
            xt, yt = mult_transfer((graph_1[i].x, graph_1[i].y, 1), -xc, -yc)
            xt, yt = mult_turn((xt, yt, 1), phi)
            graph_1[i].x, graph_1[i].y = mult_transfer((xt, yt, 1), xc, yc)

            xt, yt = mult_transfer((graph_2[i].x, graph_2[i].y, 1), -xc, -yc)
            xt, yt = mult_turn((xt, yt, 1), phi)
            graph_2[i].x, graph_2[i].y = mult_transfer((xt, yt, 1), xc, yc)

            xt, yt = mult_transfer((graph_3[i].x, graph_3[i].y, 1), -xc, -yc)
            xt, yt = mult_turn((xt, yt, 1), phi)
            graph_3[i].x, graph_3[i].y = mult_transfer((xt, yt, 1), xc, yc)
        history.append_new(get_inv_turn(xc, yc, phi))
        cr_turn(xc, yc, phi)
        redraw()


def get_inv_turn(xc, yc, phi):
    matrix_transfer1 = get_transfer_matrix(-xc, -yc)
    matrix_turn = get_turn_matrix(phi)
    matrix_transfer2 = get_transfer_matrix(xc, yc)

    m = np.dot(np.dot(matrix_transfer1, matrix_turn), matrix_transfer2)
    return np.linalg.inv(m)


def apply_matrix(matrix):
    global graph_1, graph_2, graph_3, cr, pl
    for i in range(len(graph_1)):
        graph_1[i].x, graph_1[i].y, t = np.dot((graph_1[i].x, graph_1[i].y, 1), matrix)
        graph_2[i].x, graph_2[i].y, t = np.dot((graph_2[i].x, graph_2[i].y, 1), matrix)
        graph_3[i].x, graph_3[i].y, t = np.dot((graph_3[i].x, graph_3[i].y, 1), matrix)
    cr.one.x, cr.one.y, t = np.dot((cr.one.x, cr.one.y, 1), matrix)
    cr.two.x, cr.two.y, t = np.dot((cr.two.x, cr.two.y, 1), matrix)
    cr.three.x, cr.three.y, t = np.dot((cr.three.x, cr.three.y, 1), matrix)
    for i in range(len(pl)):
        pl[i][0], pl[i][1], t = np.dot((pl[i][0], pl[i][1], 1), matrix)
    redraw()


def back_step():
    global history
    if history.is_last():
        showerror("Ошибка", "Это последнее состояние")
    else:
        apply_matrix(history.get_prev())


def forward_step():
    global history
    if history.is_first():
        showerror("Ошибка", "Это самое новое состояние")
    else:
        apply_matrix(np.linalg.inv(history.get_next()))


def polygon_points():
    global cr, graph_1, graph_2, graph_3
    x_min, y_min = min(cr.one.x, cr.two.x, cr.three.x), 0
    x_max, y_max = max(cr.one.x, cr.two.x, cr.three.x), max(cr.one.y, cr.two.y, cr.three.y)
    p = list()
    for i in range(len(graph_1)):
        if x_max >= graph_1[i].x >= x_min and y_max >= graph_1[i].y >= y_min:
            p.append([graph_1[i].x, graph_1[i].y])
    p.append([cr.one.x, cr.one.y])
    for i in range(len(graph_2)):
        if x_max >= graph_2[i].x >= x_min and y_max >= graph_2[i].y >= y_min:
            p.append([graph_2[i].x, graph_2[i].y])
    p.append([cr.two.x, cr.two.y])
    for i in range(len(graph_3) - 1, -1, -1):
        if x_max >= graph_3[i].x >= x_min and y_max >= graph_3[i].y >= y_min:
            p.append([graph_3[i].x, graph_3[i].y])
    p.append([cr.three.x, cr.three.y])

    return p


WIND_Y = wind.winfo_screenheight()
WIND_X = wind.winfo_screenwidth()

CANVAS_X = WIND_X - 480
CANVAS_Y = WIND_Y - 100

EPS = float('1e-7')

X_MIN, X_MAX = -4, 5
Y_MIN, Y_MAX = -4, 5

frame_transfer = create_frame(0, 0, 4, 4)
frame_turn = create_frame(4, 0, 4, 4)
frame_scaling = create_frame(8, 0, 4, 4)
frame_back = create_frame(12, 0, 2, 4)

ent_dx, ent_dy, btn_transfer = fill_frame(frame_transfer, "Перенос", info_transfer)
ent_xc_turn, ent_yc_turn, ent_angle, btn_turn = fill_frame(frame_turn, "Поворот", info_turn)
ent_xc_scale, ent_yc_scale, ent_kx, ent_ky, btn_scale = fill_frame(frame_scaling, "Масштабирование", info_scale)
btn_back, btn_forward = fill_frame(frame_back, "", "")
history = History()

figure = Figure(figsize=(10, 10), dpi=95)
plot = figure.add_subplot(1, 1, 1)

clear()

graph_1, graph_2, graph_3 = draw_figure()
x1, y1 = find_cross(graph_1, graph_2)
x2, y2 = find_cross(graph_2, graph_3)
x3, y3 = find_cross(graph_1, graph_3)
cr = Crossing(x1, y1, x2, y2, x3, y3)
pl = polygon_points()
redraw()

canvas = FigureCanvasTkAgg(figure, wind)
canvas.get_tk_widget().place(x=460, y=-100)

wind.mainloop()
