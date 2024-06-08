from tkinter import *
from tkinter import ttk
from tkinter.messagebox import *
from math import *

EPS = float(1e-7)


# создание поля
def create_canvas():
    canv = Canvas(wind, width=canvas_x, height=canvas_y, bg='white')
    canv.grid(row=3, column=0, columnspan=6)

    return canv


# конвертация x из изначальных координат
def convert_origin_x(x):
    return x * (x_max - x_min) / canvas_x + x_min


# конвертация y из изначальных координат
def convert_origin_y(y):
    return -(y * (y_max - y_min) / canvas_y - y_max)


# отрисовка осей
def draw_axis():
    # отрисовка оси y
    for i in range(0, canvas_y - axis_space, 50):
        canvas.create_line(7, canvas_y - axis_space - i, 15, canvas_y - i - axis_space, width=2)  # черточки
        if i != 0:
            canvas.create_text(30, canvas_y - i - axis_space,
                               text=str(round(convert_origin_y(canvas_y - i - axis_space), 2)))  # подписи

    # отрисовка оси x
    for i in range(0, canvas_x - axis_space, 50):
        canvas.create_line(i + axis_space, canvas_y - 15, i + axis_space, canvas_y - 7, width=2)  # черточки
        if i != 0:
            canvas.create_text(i + axis_space, canvas_y - axis_space - 10,
                               text=round(convert_origin_x(i + axis_space), 2))  # подписи

    # отрисовка стрелочек
    canvas.create_line(0, canvas_y - axis_space, canvas_x, canvas_y - axis_space, width=2, arrow=LAST)
    canvas.create_line(axis_space, canvas_y - axis_space, axis_space, 0, width=2, arrow=LAST)


# создание таблицы
def create_table(columns):
    tbl = ttk.Treeview(columns=columns, show="headings")
    tbl.grid(row=0, column=0, rowspan=3, columnspan=3, padx=25, pady=15)
    style_tbl = ttk.Style()
    style_tbl.configure("Treeview.Heading", font=("Arial bold", 14))
    style_tbl.configure("Treeview", font=("Arial", 12))

    for i in range(len(columns)):
        tbl.heading(columns[i], text=columns[i])
        tbl.column(f"#{i + 1}", anchor=CENTER)

    tbl.column("#1", width=100)
    tbl.column("#2", width=250)
    tbl.column("#3", width=250)

    return tbl


# удаление построенного треугольника
def reset_canvas():
    canvas.delete("all")
    draw_axis()
    for p in points:
        draw_point(p[1], p[2], p[0], "black")


# добавление точки
def add_point():
    try:
        x = float(x_ent.get())
        y = float(y_ent.get())
    except ValueError:
        showerror("Ошибка", "Введены некорректные данные")
    else:
        if len(canvas.find_withtag("line")) != 0:
            reset_canvas()
        if len(points) == 0:
            num = 1
        else:
            num = points[-1][0] + 1
        points.append(tuple([num, x, y]))
        table.insert("", index=num - 1, values=points[-1])
        clear_entries()

        draw_point(x, y, num, "purple")


# изменение номеров после удаления
def change_nums():
    # изменение значений на поле
    k = 1
    for p in points:
        point = canvas.find_withtag("n" + str(p[0]))
        canvas.itemconfigure(point, tags=tuple(["point", "n" + str(k)]))

        point_text = canvas.find_withtag("t" + str(p[0]))
        canvas.itemconfigure(point_text, tags=tuple(["text", "t" + str(k)]),
                             text=str(k) + ". (" + str(p[1]) + "; " + str(p[2]) + ")")
        k += 1

    # изменение значений в таблице
    k = 1
    for line in table.get_children():
        temp = table.item(line)['values']
        table.item(line, values=(k, temp[1], temp[2]))
        points[k - 1] = tuple([k, points[k - 1][1], points[k - 1][2]])
        k += 1


# удаление точки
def del_point():
    if not table.selection():
        showerror("Ошибка", "Точки для удаления не выделены")
    else:
        if len(canvas.find_withtag("line")) != 0:
            reset_canvas()
        for i in table.selection():
            item = table.item(i)['values']
            item = tuple([item[0], float(item[1]), float(item[2])])
            del points[points.index(tuple(item))]
            table.delete(i)
            erase_point(item[0])
        change_nums()


# изменение координат точки
def change_point():
    if not table.selection():
        showerror("Ошибка", "Точка для изменения не выделена")
    elif len(table.selection()) != 1:
        showerror("Ошибка", "Необходимо выбрать одну точку")
    else:
        if len(canvas.find_withtag("line")) != 0:
            reset_canvas()
        item = table.item(table.selection()[0])['values']
        try:
            x = float(x_ent.get())
            y = float(y_ent.get())
        except ValueError:
            showerror("Ошибка", "Введены некорректные координаты")
        else:
            table.item(table.selection()[0], values=tuple([item[0], x, y]))
            points[item[0] - 1] = tuple([item[0], x, y])
            erase_point(item[0])
            draw_point(x, y, item[0], "purple")
            clear_entries()


# очистка полей ввода
def clear_entries():
    x_ent.delete(0, END)
    y_ent.delete(0, END)


# создание кнопки
def create_button(btn_name, row, column, cmd, width):
    btn = Button(text=btn_name, command=cmd, font="Arial 14", width=width, height=2, bg="#fffafa")
    btn.grid(row=row, column=column, padx=10, pady=1)

    return btn


# создание поля ввода
def create_entry(row, column, side):
    ent = Entry(wind, font="Arial 14", width=10)
    ent.grid(row=row, column=column, padx=1, pady=1, sticky=side)

    return ent


# создание надписи
def create_label(text, row, column, side):
    lb = Label(text=text, font="Arial 14")
    lb.grid(row=row, column=column, padx=1, pady=1, sticky=side)

    return lb


# удаление точки с полотна
def erase_point(num):
    canvas.delete(canvas.find_withtag("n" + str(num)))
    canvas.delete(canvas.find_withtag("t" + str(num)))


# отрисовка точки
def draw_point(x, y, num, color):
    xp, yp = convert_x(x), convert_y(y)
    canvas.create_oval(xp - 3, yp - 3, xp + 3, yp + 3, fill=color, tags=tuple(["point", "n" + str(num)]))
    point_lb = str(num) + ". (" + str(round(x, 2)) + "; " + str(round(y, 2)) + ")"
    canvas.create_text(xp, yp + 10, text=point_lb, tags=tuple(["text", "t" + str(num)]))


# конвертация x (масштабирование)
def convert_x(x):
    try:
        return (x - x_min) / (x_max - x_min) * canvas_x
    except ZeroDivisionError:
        return (x - x_min) * canvas_x


# конвертация y (масштабирование)
def convert_y(y):
    try:
        return (y_max - y) / (y_max - y_min) * canvas_y
    except ZeroDivisionError:
        return (y_max - y) * canvas_y


# отрисовка линии
def draw_line(x1, y1, x2, y2, color):
    canvas.create_line(convert_x(x1), convert_y(y1), convert_x(x2), convert_y(y2), fill=color, width=2, tags="line")


# проверка, лежат ли 3 точки на одной прямой
def is_on_line(x1, y1, x2, y2, x3, y3):
    return abs((x3 - x1) * (y2 - y1) - (x2 - x1) * (y3 - y1)) < EPS


# проверка, лежат ли все точки на одной прямой
def is_on_line_all():
    for i in range(len(points) - 2):
        for j in range(i + 1, len(points) - 1):
            for k in range(j + 1, len(points)):
                x1, x2, x3 = points[i][1], points[j][1], points[k][1]
                y1, y2, y3 = points[i][2], points[j][2], points[k][2]
                if not is_on_line(x1, y1, x2, y2, x3, y3):  # нашлись 3 точки не на одной прямой
                    return False
    return True


# длина вектора по координатам
def vector_len(x1, y1, x2, y2):
    return sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)


# длина биссектрисы, проведенной из точки b
def bisector_len(a, b, c):
    p = (a + b + c) / 2
    return (2 * sqrt(a * c * p * (p - b))) / (a + c)


# отрисовка треугольника
def draw_triangle(x1, y1, x2, y2, x3, y3):
    draw_line(x1, y1, x2, y2, "blue")
    draw_line(x2, y2, x3, y3, "blue")
    draw_line(x3, y3, x1, y1, "blue")


# координаты точки пересечения биссектрисы из точки а и bc
def bisector_coords(bx, by, cx, cy, ab, ac):
    x = (ac * bx + ab * cx) / (ab + ac)
    y = (ac * by + ab * cy) / (ab + ac)
    return x, y


# поиск треугольника с минимальной длиной биссектрисы
def find_triangle():
    global x_min, x_max, y_min, y_max, x_c, y_c
    if len(points) < 3:
        showerror("Ошибка", "Точек недостаточно для построения треугольника")
    elif is_on_line_all():
        showerror("Ошибка", "Все точки лежат на одной прямой.\nНевозможно построить треугольник")
    else:
        n_points = len(points)
        min_bes_len = ae = be = ce = float("inf")
        x1_find = x2_find = x3_find = 0
        y1_find = y2_find = y3_find = 0

        for i in range(n_points - 2):
            for j in range(i + 1, n_points - 1):
                for k in range(j + 1, n_points):
                    x1, x2, x3 = points[i][1], points[j][1], points[k][1]
                    y1, y2, y3 = points[i][2], points[j][2], points[k][2]

                    # не рассматриваем вырожденный случай
                    if is_on_line(x1, y1, x2, y2, x3, y3):
                        continue

                    a = vector_len(x1, y1, x2, y2)
                    b = vector_len(x2, y2, x3, y3)   # длины сторон
                    c = vector_len(x3, y3, x1, y1)

                    xd, yd = bisector_coords(x2, y2, x3, y3, a, c)
                    ae = vector_len(x1, y1, xd, yd)
                    xd, yd = bisector_coords(x3, y3, x1, y1, b, a)
                    be = vector_len(x2, y2, xd, yd)
                    xd, yd = bisector_coords(x1, y1, x2, y2, c, b)
                    ce = vector_len(x3, y3, xd, yd)

                    # запоминаем треугольник с минимальной биссектрисой
                    if min(ae, be, ce) < min_bes_len:
                        min_bes_len = min(ae, be, ce)
                        x1_find, x2_find, x3_find = x1, x2, x3
                        y1_find, y2_find, y3_find = y1, y2, y3

        # пересчет масштаба
        x_min = min(x1_find, x2_find, x3_find)
        y_min = min(y1_find, y2_find, y3_find)
        x_max = max(x1_find, x2_find, x3_find)
        y_max = max(y1_find, y2_find, y3_find)

        # Отступ от краев поля графика
        x_c = (x_min + x_max) / 2
        x_min = x_c - (x_c - x_min) * (kx_space + x_max / canvas_x + 0.3)
        x_max = x_c + (x_max - x_c) * (kx_space + x_max / canvas_x + 0.3)

        y_c = (y_min + y_max) / 2
        y_min = y_c - (y_c - y_min) * (ky_space + y_max / canvas_y + 0.3)
        y_max = y_c + (y_max - y_c) * (ky_space + y_max / canvas_y + 0.3)

        # Коэффициенты доли в экране
        kx = (x_max - x_min) / canvas_x
        ky = (y_max - y_min) / canvas_y

        if kx < ky:
            # Координаты центра растяжения
            if kx != 0:
                x_c = (x_min + x_max) / 2
                x_min = x_c - (x_c - x_min) * (ky / kx)
                x_max = x_c + (x_max - x_c) * (ky / kx)
            else:
                x_c = (x_min + x_max) / 2
                x_min = x_c - (x_c - x_min) * ky
                x_max = x_c + (x_max - x_c) * ky
        else:
            # Координаты центра растяжения
            if ky != 0:
                y_c = (y_min + y_max) / 2
                y_min = y_c - (y_c - y_min) * (kx / ky)
                y_max = y_c + (y_max - y_c) * (kx / ky)
            else:
                y_c = (y_min + y_max) / 2
                y_min = y_c - (y_c - y_min) * kx
                y_max = y_c + (y_max - y_c) * kx

        reset_canvas()
        draw_triangle(x1_find, y1_find, x2_find, y2_find, x3_find, y3_find)

        a = vector_len(x1_find, y1_find, x2_find, y2_find)
        b = vector_len(x2_find, y2_find, x3_find, y3_find)  # длины сторон
        c = vector_len(x3_find, y3_find, x1_find, y1_find)

        xd, yd = bisector_coords(x2_find, y2_find, x3_find, y3_find, a, c)
        ae = vector_len(x1_find, y1_find, xd, yd)
        xd, yd = bisector_coords(x3_find, y3_find, x1_find, y1_find, b, a)
        be = vector_len(x2_find, y2_find, xd, yd)
        xd, yd = bisector_coords(x1_find, y1_find, x2_find, y2_find, c, b)
        ce = vector_len(x3_find, y3_find, xd, yd)

        # отрисовка биссектрисы
        if abs(min_bes_len - ae) < EPS:
            xd, yd = bisector_coords(x2_find, y2_find, x3_find, y3_find, a, c)
            draw_line(x1_find, y1_find, xd, yd, "red")
            draw_point(xd, yd, "E", "black")
        elif abs(min_bes_len - be) < EPS:
            xd, yd = bisector_coords(x3_find, y3_find, x1_find, y1_find, b, a)
            draw_line(x2_find, y2_find, xd, yd, "red")
            draw_point(xd, yd, "E", "black")
        else:
            xd, yd = bisector_coords(x1_find, y1_find, x2_find, y2_find, c, b)
            draw_line(x3_find, y3_find, xd, yd, "red")
            draw_point(xd, yd, "E", "black")

        showinfo("Результат", f"Треугольник состоит из точек с координатами:\n({x1_find}; {y1_find})\n"
                              f"({x2_find}; {y2_find})\n({x3_find}; {y3_find})\nНаименьшая биссектриса имеет длину: "
                              f"{round(min(ae, be, ce), 2)}\n\nДлины всех биссектрис:\n1) {round(ae, 2)}\n2) {round(be, 2)}"
                              f"\n3) {round(ce, 2)}")


# вывод сообщения с уловием задачи
def show_task():
    message = "На плоскости задано множество точек.\nНайти такой треугольник с вершинами в этих точках, " \
              "у которого биссектриса имеет минимальную длину.\nДля каждого треугольника берется та из трех " \
              "биссектрис, длина которой минимальна."
    showinfo("Условие задачи", message)


# создание окна
wind = Tk()
wind.state('zoomed')
wind.title('Lab 1')

wind_w = wind.winfo_screenwidth()
wind_h = wind.winfo_screenheight()
wind.option_add('*Dialog.msg.font', 'Arial 14')

# параметры поля
canvas_x = wind_w
canvas_y = wind_h - 350
axis_space = 15
kx_space = 1.01
ky_space = 1.02

# массив точек и таблица точек
points = []
table = create_table(("№", "x", "y"))

# создание полей ввода
x_ent = create_entry(1, 3, N)
y_ent = create_entry(1, 3, S)

# создание надписей
info_lb = create_label("Координаты: ", 0, 3, W)
x_lb = create_label("X: ", 1, 3, NW)
y_lb = create_label("Y: ", 1, 3, SW)

# создание кнопок
add_btn = create_button("Добавить точку", 0, 4, add_point, 35)
del_btn = create_button("Удалить точку", 1, 4, del_point, 35)
chg_btn = create_button("Изменить координаты", 2, 4, change_point, 35)
find_btn = create_button("Найти треугольник", 2, 3, find_triangle, 20)

# выбор первоначального масштаба
x_max, x_min = 30, 0
y_max, y_min = 10, 0

x_c = (x_min + x_max) / 2
x_min = x_c - (x_c - x_min) * kx_space
x_max = x_c + (x_max - x_c) * kx_space

y_c = (y_min + y_max) / 2
y_min = y_c - (y_c - y_min) * ky_space
y_max = y_c + (y_max - y_c) * ky_space

menubar = Menu(wind)
menu_help = Menu(menubar, tearoff=0)
menubar.add_cascade(menu=menu_help, label='Задание')
menu_help.add_command(label='Условие', command=show_task)

canvas = create_canvas()
draw_axis()

wind.config(menu=menubar)
wind.mainloop()
