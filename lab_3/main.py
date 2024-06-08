from tkinter import *
from tkinter import colorchooser
from std_draw import *
from cda import *
from brezenhem import *
from vu import *
from tkinter.messagebox import *
import matplotlib.pyplot as plt
import numpy as np

wind = Tk()
wind.state('zoomed')
wind.title('Lab 3')

CANVAS_WIDTH, CANVAS_HEIGHT = 1160, 780


def step_bar():
    close_plt()

    angle = 0
    step = 1
    pb = [0, 0]
    pe = [pb[0], pb[1] + 1000]

    angles = []
    DDA_steps = []
    BrezenhemInteger_steps = []
    BrezenhemFloat_steps = []
    BrezenhemSmooth_steps = []
    VU_steps = []

    for j in range(90):
        DDA_steps.append(draw_cda(canvas, pb[0], pb[1], round(pe[0]), round(pe[1]), cur_line_color, stepmode=True, draw=False))
        BrezenhemInteger_steps.append(draw_brezenhem_int(canvas, pb[0], pb[1], round(pe[0]), round(pe[1]), cur_line_color, stepmode=True, draw=False))
        BrezenhemFloat_steps.append(draw_brezenhem_float(canvas, pb[0], pb[1], round(pe[0]), round(pe[1]), cur_line_color, stepmode=True, draw=False))
        BrezenhemSmooth_steps.append(draw_brezenhem_gradation(canvas, pb[0], pb[1], round(pe[0]), round(pe[1]), cur_line_color,
                                                              cur_bg_color, stepmode=True, draw=False))
        VU_steps.append(draw_vu(canvas, pb[0], pb[1], round(pe[0]), round(pe[1]), cur_line_color, cur_bg_color, stepmode=True, draw=False))

        pe[0], pe[1] = turn_point(pb[0], pb[1], pe[0], pe[1], radians(step))
        angles.append(angle)
        angle += step

    plt.figure("Исследование ступенчатости алгоритмов построения", figsize=(18, 10))

    plt.subplot(2, 3, 1)
    plt.plot(angles, DDA_steps, label="ЦДА")
    plt.plot(angles, BrezenhemFloat_steps, '--', label="Брензенхем с действительными коэффицентами")
    plt.plot(angles, BrezenhemInteger_steps, '--', label="Брензенхем с целыми коэффицентами")
    plt.plot(angles, BrezenhemSmooth_steps, '.', label="Брензенхем с устр\nступенчатости")
    plt.plot(angles, VU_steps, '-.', label="By")
    plt.title("Исследование ступенчатости")
    plt.xticks(np.arange(91, step=5))
    plt.legend()
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 2)
    plt.title("ЦДА")
    plt.plot(angles, DDA_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 3)
    plt.title("BУ")
    plt.plot(angles, VU_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 4)
    plt.title("Брензенхем с действительными коэффицентами")
    plt.plot(angles, BrezenhemFloat_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 5)
    plt.title("Брензенхем с целыми коэффицентами")
    plt.plot(angles, BrezenhemInteger_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.subplot(2, 3, 6)
    plt.title("Брензенхем с устр. ступенчатости")
    plt.plot(angles, BrezenhemSmooth_steps)
    plt.xticks(np.arange(91, step=5))
    plt.ylabel("Количество ступенек")
    plt.xlabel("Угол в градусах")

    plt.show()


# гистограмма времени
def time_bar():
    close_plt()

    plt.figure("Исследование времени работы алгоритмов построения.", figsize=(9, 7))
    times = [0] * 5

    for i in range(10):
        times[0] += draw_spector_by_alg(canvas, 375, 200, 500, 1, cur_line_color, draw_cda, draw=False)
        times[1] += draw_spector_by_alg(canvas, 375, 200, 500, 1, cur_line_color, draw_brezenhem_float, draw=False)
        times[2] += draw_spector_by_alg(canvas, 375, 200, 500, 1, cur_line_color, draw_brezenhem_int, draw=False)
        times[3] += draw_spector_by_alg(canvas, 375, 200, 500, 1, cur_line_color, draw_brezenhem_gradation, draw=False,
                                         intensive=cur_bg_color)
        times[4] += draw_spector_by_alg(canvas, 375, 200, 500, 1, cur_line_color, draw_vu, draw=False,
                                         intensive=cur_bg_color)

    for i in range(len(times)):
        times[i] *= 10

    Y = range(len(times))
    L = ['ЦДА', 'Брезенхем\n(float)',
         'Брезенхем \n(int)', 'Брезенхем\nс устранением\nступенчатости', 'Ву']
    plt.bar(Y, times, align='center')
    plt.xticks(Y, L)
    plt.ylabel("Cекунды")
    plt.show()


def close_plt():
    plt.figure("Исследование времени работы алгоритмов построения.",)
    plt.close()
    plt.figure("Исследование ступенчатости алгоритмов построение.")
    plt.close()


def clear_canvas():
    global canvas, CANVAS_WIDTH, CANVAS_HEIGHT
    canvas.delete('all')
    draw_axis(canvas, CANVAS_WIDTH, CANVAS_HEIGHT)


def draw_spector_handler():
    global algorithm, canvas, cur_line_color, cur_bg_color
    xc, yc = xc_ent.get(), yc_ent.get()
    length, angle = len_ent.get(), angle_ent.get()
    try:
        xc, yc = int(xc), int(yc)
        length, angle = int(length), float(angle)
    except ValueError:
        showerror("Ошибка", "Введены некорректные данные")
    else:
        if algorithm.get() == 0:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_cda)
        elif algorithm.get() == 1:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_brezenhem_float)
        elif algorithm.get() == 2:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_brezenhem_int)
        elif algorithm.get() == 3:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_brezenhem_gradation,
                                intensive=cur_bg_color)
        elif algorithm.get() == 4:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_vu, intensive=cur_bg_color)
        elif algorithm.get() == 5:
            draw_spector_by_alg(canvas, xc, yc, length, angle, cur_line_color, draw_standard_line)


def draw_line_handler():
    global algorithm, canvas, cur_line_color, cur_bg_color
    xn, yn = xn_ent.get(), yn_ent.get()
    xk, yk = xk_ent.get(), yk_ent.get()
    try:
        xn, yn = int(xn), int(yn)
        xk, yk = int(xk), int(yk)
    except ValueError:
        showerror("Ошибка", "Введены некорректные координаты концов отрезка")
    else:
        if algorithm.get() == 0:
            draw_cda(canvas, xn, yn, xk, yk, cur_line_color)
        elif algorithm.get() == 1:
            draw_brezenhem_float(canvas, xn, yn, xk, yk, cur_line_color)
        elif algorithm.get() == 2:
            draw_brezenhem_int(canvas, xn, yn, xk, yk, cur_line_color)
        elif algorithm.get() == 3:
            draw_brezenhem_gradation(canvas, xn, yn, xk, yk, cur_line_color, cur_bg_color)
        elif algorithm.get() == 4:
            draw_vu(canvas, xn, yn, xk, yk, cur_line_color, cur_bg_color)
        elif algorithm.get() == 5:
            draw_standard_line(canvas, xn, yn, xk, yk, cur_line_color)


def get_bg_color():
    color_code = colorchooser.askcolor(title="Выберите цвет фона")
    set_bg_color(color_code[-1])


def set_bg_color(color):
    global cur_bg_color
    cur_bg_color = color
    canvas.configure(bg=color)


def get_line_color():
    color_code = colorchooser.askcolor(title="Выберите цвет линии")
    set_line_color(color_code[-1])


def set_line_color(color):
    global cur_line_color, lb_color
    cur_line_color = color
    lb_color.configure(bg=color)


canvas = Canvas(wind, bg='white', height=CANVAS_HEIGHT, width=CANVAS_WIDTH)
canvas.place(x=350, y=3)
cur_bg_color = 'white'


frm_alg = Frame(wind, bg='white')
frm_alg.grid(row=0, column=0, rowspan=7, columnspan=6, padx=10, pady=3, sticky=EW)
Label(frm_alg, text="Алгоритмы построения", font="Arial 17", bg='black', fg='white', width=24).grid(row=0, column=0,
                                                                                                    columnspan=6,
                                                                                                    sticky=NSEW)
algorithm = IntVar()
algorithm.set(0)
Radiobutton(frm_alg, text="Цифровой дифференциальный анализ", bg='white', font="arial 12", anchor=W,
            variable=algorithm, value=0).grid(row=1, column=0, columnspan=6, sticky=EW)
Radiobutton(frm_alg, text="Брезенхем (float)", bg='white', font="arial 12", anchor=W,
            variable=algorithm, value=1).grid(row=2, column=0, columnspan=6, sticky=EW)
Radiobutton(frm_alg, text="Брезенхем (integer)", bg='white', font="arial 12", anchor=W,
            variable=algorithm, value=2).grid(row=3, column=0, columnspan=6, sticky=EW)
Radiobutton(frm_alg, text="Брезенхем\n(с устранением ступенчатости)", bg='white', font="arial 12", justify=LEFT,
            anchor=W,
            variable=algorithm, value=3).grid(row=4, column=0, columnspan=6, sticky=EW)
Radiobutton(frm_alg, text="Ву", bg='white', font="arial 12", anchor=W,
            variable=algorithm, value=4).grid(row=5, column=0, columnspan=6, sticky=EW)
Radiobutton(frm_alg, text="Библиотечная функция", bg='white', font="arial 12", anchor=W,
            variable=algorithm, value=5).grid(row=6, column=0, columnspan=6, sticky=EW)

frm_color = Frame(wind, bg='white')
frm_color.grid(row=8, column=0, rowspan=8, columnspan=6, padx=10, pady=3, sticky=EW)
Label(frm_color, text="Выбор цвета", font="Arial 17", bg='black', fg='white', width=24).grid(row=0, column=0,
                                                                                             columnspan=6,
                                                                                             sticky=EW)

Label(frm_color, text="Цвет фона", font="Arial 12", bg='white').grid(row=1, column=0, columnspan=6, sticky=NSEW)
Button(frm_color, bg="white", activebackground="white", command=lambda: set_bg_color("white")).grid(row=2, column=0,
                                                                                                    sticky=NSEW)
Button(frm_color, bg="black", activebackground="black", command=lambda: set_bg_color("black")).grid(row=2, column=1,
                                                                                                    sticky=NSEW)
Button(frm_color, bg="yellow", activebackground="yellow", command=lambda: set_bg_color("yellow")).grid(row=2, column=2,
                                                                                                       sticky=NSEW)
Button(frm_color, bg="orange", activebackground="orange", command=lambda: set_bg_color("orange")).grid(row=2, column=3,
                                                                                                       sticky=NSEW)
Button(frm_color, bg="red", activebackground="red", command=lambda: set_bg_color("red")).grid(row=2, column=4,
                                                                                              sticky=NSEW)
Button(frm_color, bg="purple", activebackground="purple", command=lambda: set_bg_color("purple")).grid(row=2, column=5,
                                                                                                       sticky=NSEW)
Button(frm_color, bg='white', text='Выбрать другой цвет фона', font="Arial 12", command=get_bg_color).grid(row=3,
                                                                                                           column=0,
                                                                                                           columnspan=6)
Label(frm_color, text="Цвет линии", font="Arial 12", bg='white').grid(row=4, column=0, columnspan=6)
Button(frm_color, bg="white", activebackground="white", command=lambda: set_line_color("white")).grid(row=5, column=0,
                                                                                                      sticky=NSEW)
Button(frm_color, bg="black", activebackground="black", command=lambda: set_line_color("black")).grid(row=5, column=1,
                                                                                                      sticky=NSEW)
Button(frm_color, bg="yellow", activebackground="yellow", command=lambda: set_line_color("yellow")).grid(row=5,
                                                                                                         column=2,
                                                                                                         sticky=NSEW)
Button(frm_color, bg="orange", activebackground="orange", command=lambda: set_line_color("orange")).grid(row=5,
                                                                                                         column=3,
                                                                                                         sticky=NSEW)
Button(frm_color, bg="red", activebackground="red", command=lambda: set_line_color("red")).grid(row=5, column=4,
                                                                                                sticky=NSEW)
Button(frm_color, bg="purple", activebackground="purple", command=lambda: set_line_color("purple")).grid(row=5,
                                                                                                         column=5,
                                                                                                         sticky=NSEW)
Button(frm_color, bg='white', text='Выбрать другой цвет линии', font="Arial 12", command=get_line_color).grid(
    row=6,
    column=0,
    columnspan=6)
cur_line_color = 'black'
Label(frm_color, text="Текущий цвет линии:", font="Arial 12", bg='white').grid(row=7, column=0, columnspan=3,
                                                                               sticky=E)
lb_color = Label(frm_color, bg=cur_line_color, borderwidth=3, relief="sunken")
lb_color.grid(row=7, column=3, sticky=NSEW)

frm_line = Frame(wind, bg='white')
frm_line.grid(row=16, column=0, rowspan=4, columnspan=6, padx=10, pady=3, sticky=NSEW)
Label(frm_line, text="Построение линии", font="Arial 17", bg='black', fg='white', width=24).grid(row=0, column=0,
                                                                                                 columnspan=6,
                                                                                                 sticky=NSEW)

Label(frm_line, text="Хн", font="Arial 12", bg='white').grid(row=1, column=0, columnspan=1, sticky=NSEW)
Label(frm_line, text="Yн", font="Arial 12", bg='white').grid(row=1, column=1, columnspan=1, sticky=NSEW)
Label(frm_line, text="Хк", font="Arial 12", bg='white').grid(row=1, column=2, columnspan=1, sticky=NSEW)
Label(frm_line, text="Yк", font="Arial 12", bg='white').grid(row=1, column=3, columnspan=1, sticky=NSEW)

xn_ent = Entry(frm_line, font="Arial 12", bg='white', width=8)
xn_ent.grid(row=2, column=0, columnspan=1, sticky=W)
yn_ent = Entry(frm_line, font="Arial 12", bg='white', width=8)
yn_ent.grid(row=2, column=1, columnspan=1, sticky=W)
xk_ent = Entry(frm_line, font="Arial 12", bg='white', width=8)
xk_ent.grid(row=2, column=2, columnspan=1, sticky=W)
yk_ent = Entry(frm_line, font="Arial 12", bg='white', width=8)
yk_ent.grid(row=2, column=3, columnspan=1, sticky=W)

Button(frm_line, text="Построить линию", command=draw_line_handler, font="Arial 12", bg='white').grid(row=3, column=0,
                                                                                                      sticky=NSEW,
                                                                                                      columnspan=6)

frm_spector = Frame(wind, bg='white')
frm_spector.grid(row=20, column=0, rowspan=4, columnspan=6, padx=10, pady=3)
Label(frm_spector, text="Построение спектра", font="Arial 17", bg='black', fg='white', width=24).grid(row=0, column=0,
                                                                                                      columnspan=6,
                                                                                                      sticky=NSEW)
Label(frm_spector, text="Xc", font="Arial 12", bg='white').grid(row=1, column=0, columnspan=1, sticky=NSEW)
Label(frm_spector, text="Yc", font="Arial 12", bg='white').grid(row=1, column=1, columnspan=1, sticky=NSEW)
Label(frm_spector, text="Длина", font="Arial 12", bg='white').grid(row=1, column=2, columnspan=1, sticky=NSEW)
Label(frm_spector, text="Шаг угла", font="Arial 12", bg='white').grid(row=1, column=3, columnspan=1, sticky=NSEW)

xc_ent = Entry(frm_spector, font="Arial 12", bg='white', width=8)
xc_ent.grid(row=2, column=0, columnspan=1, sticky=W)
yc_ent = Entry(frm_spector, font="Arial 12", bg='white', width=8)
yc_ent.grid(row=2, column=1, columnspan=1, sticky=W)
len_ent = Entry(frm_spector, font="Arial 12", bg='white', width=8)
len_ent.grid(row=2, column=2, columnspan=1, sticky=W)
angle_ent = Entry(frm_spector, font="Arial 12", bg='white', width=8)
angle_ent.grid(row=2, column=3, columnspan=1, sticky=W)

Button(frm_spector, text="Построить спектр", command=draw_spector_handler, font="Arial 12", bg='white').grid(row=3, column=0, columnspan=6,
                                                                               sticky=NSEW)

frm_time = Frame(wind, bg='white')
frm_time.grid(row=24, column=0, rowspan=3, columnspan=6, padx=10, pady=3, sticky=NSEW)

Button(frm_time, text="Сравнение времени", command=time_bar, font="Arial 12", bg='white', width=34).grid(row=0,
                                                                                    column=0, columnspan=6, sticky=NSEW)
Button(frm_time, text="Сравнение ступенчатости", command=step_bar, font="Arial 12", bg='white').grid(row=1, column=0, columnspan=6,
                                                                                   sticky=NSEW)
Button(frm_time, text="Очистить экран", command=clear_canvas, font="Arial 12", bg='white').grid(row=2, column=0, columnspan=6, sticky=NSEW)


draw_axis(canvas, CANVAS_WIDTH, CANVAS_HEIGHT)

wind.mainloop()
