import tkinter as tk
from tkinter import colorchooser, messagebox

from config import *
from draw import add_line, set_pixel, \
    add_vertex_clipper, close_clipper
from algorithm import check_convexity_polygon, cyrus_beck_alg

root = tk.Tk()
root.title("КГ Лабораторная работа №8 \"Алгоритм Кируса-Бека\"")
root["bg"] = MAIN_COLOR
root.state('zoomed')

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)

lines = []
clipper_figure = []
is_set_rectangle = False


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def click_right(event, line_list, canvas, linecolor):
    x = event.x
    y = event.y

    if len(line_list) == 0 or len(line_list[-1]) > 2:
        line_list.append([])

    set_pixel(canvas, x, y, linecolor)

    line_list[-1].append([x, y])

    if len(line_list[-1]) == 2:
        canvas.create_line(line_list[-1][0], line_list[-1][1], fill=linecolor)

        line_list[-1].append(linecolor)


def click_middle():
    global is_set_rectangle
    if len(clipper_figure) < 3:
        messagebox.showwarning('Ошибка ввода!',
                               'Отсекатель не может состоять из вершин меньше 3!')
        return

    is_set_rectangle = True
    close_clipper(canvasField, clipper_figure, CLIPPER_COLOR)


def click_left(event):
    global is_set_rectangle
    if is_set_rectangle:
        clipper_figure.clear()
        canvasField.delete("all")
        for line in lines:
            if len(line) > 1:
                canvasField.create_line(line[0], line[1], fill=LINE_COLOR)
        is_set_rectangle = False

    add_vertex_clipper(canvasField, clipper_figure, [event.x, event.y], CLIPPER_COLOR)


def add_parallel_lines():
    if not clipper_figure:
        messagebox.showerror("Ошибка", "Отсутствует отсекатель")
        return
    for i in range(len(clipper_figure) - 1):
        x1 = clipper_figure[i][0]
        y1 = clipper_figure[i][1]
        x2 = clipper_figure[i + 1][0]
        y2 = clipper_figure[i + 1][1]

        dx = x2 - x1
        dy = y2 - y1
        k = (y2 - y1) / (x2 - x1)

        def find_parallel(_k, _x1, _y1, _x2):
            return _y1 + _k * (_x2 - _x1)

        if dx > dy:
            lines.append([[x1, y1 + 0.5 * dy], [x2, find_parallel(k, x1, y1 + 0.5 * dy, x2)], LINE_COLOR])
            lines.append([[x1, y1 - 0.5 * dy], [x2, find_parallel(k, x1, y1 - 0.5 * dy, x2)], LINE_COLOR])
            canvasField.create_line(x1, y1 + 0.5 * dy, x2, find_parallel(k, x1, y1 + 0.5 * dy, x2), fill=LINE_COLOR)
            canvasField.create_line(x1, y1 - 0.5 * dy, x2, find_parallel(k, x1, y1 - 0.5 * dy, x2), fill=LINE_COLOR)


def cut_off_command():
    if not clipper_figure:
        messagebox.showinfo("Ошибка!", "Отсутствует отсекатель")
        return
    if not check_convexity_polygon(clipper_figure):
        messagebox.showinfo("Ошибка!", "Отсекатель невыпуклый! Ожидалось, что отсекатель будет выпуклым!")
        return

    canvasField.create_polygon(clipper_figure, outline=CLIPPER_COLOR, fill=CANVAS_COLOR)

    for line in lines:
        if len(line) > 1:
            cyrus_beck_alg(canvasField, clipper_figure, line, RESULT_COLOR)


def clear_canvas():
    global is_set_rectangle
    canvasField.delete("all")
    lines.clear()
    is_set_rectangle = False
    clipper_figure.clear()


def draw_line():
    x_start = xnEntry.get()
    y_start = ynEntry.get()
    x_end = xkEntry.get()
    y_end = ykEntry.get()

    if not x_start or not y_start:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты начала отрезка!')
    elif not x_end or not y_end:
        messagebox.showwarning('Ошибка ввода',
                               'Не заданы координаты конца отрезка!')
    else:
        try:
            x_start, y_start = int(x_start), int(y_start)
            x_end, y_end = int(x_end), int(y_end)
        except all:
            messagebox.showwarning('Ошибка ввода',
                                   'Координаты заданы неверно!')
            return

        add_line(canvasField, lines, x_start, y_start, x_end, y_end, LINE_COLOR)


def draw_vertex():
    global is_set_rectangle
    x_clipper = xclEntry.get()
    y_clipper = yclEntry.get()

    if not x_clipper or not y_clipper:
        messagebox.showwarning('Ошибка ввода!',
                               'Не заданы координаты вершина отсекателя!')
        return

    try:
        x_clipper = int(x_clipper)
        y_clipper = int(y_clipper)
    except all:
        messagebox.showwarning('Ошибка ввода',
                               'Координаты заданы неверно!\n'
                               'Ожидался ввод целочисленных данных!')
        return

    if is_set_rectangle:
        clipper_figure.clear()
        canvasField.delete("all")
        for line in lines:
            if len(line) > 1:
                canvasField.create_line(line[0], line[1], fill=LINE_COLOR)
        is_set_rectangle = False

    add_vertex_clipper(canvasField, clipper_figure, [x_clipper, y_clipper], CLIPPER_COLOR)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT DATA FRAME
dataFrame = tk.Frame(root, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT)
dataFrame["bg"] = MAIN_FRAME_COLOR

dataFrame.pack(side=tk.LEFT, padx=BORDERS_SPACE, fill=tk.Y)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ВЫБОР цвета

chooseColorMainLabel = tk.Label(dataFrame, bg=MAIN_COLOR_LABEL_BG, text="ВЫБОР ЦВЕТА",
                                font=("Consolas", 14), fg=MAIN_COLOR_LABEL_TEXT, relief=tk.SOLID)

size = (DATA_FRAME_WIGHT // 1.7) // 8
chooseColorMainLabel.place(x=0, y=0, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# выбор цвета отрезка

lineColorLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет отрезка:",
                          font=("Consolas", 14),
                          fg=MAIN_COLOR_LABEL_TEXT)

lineCurColorTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет отрезка:",
                                 font=("Consolas", 13),
                                 fg=MAIN_COLOR_LABEL_TEXT)

lineCurColorLabel = tk.Label(dataFrame, bg="black")


def get_color_line():
    color_code = colorchooser.askcolor(title="Choose color line")
    set_linecolor(color_code[-1])


def set_linecolor(color):
    global LINE_COLOR
    LINE_COLOR = color
    lineCurColorLabel.configure(bg=LINE_COLOR)


whiteLine = tk.Button(dataFrame, bg="white", activebackground="white",
                      command=lambda: set_linecolor("white"))
yellowLine = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                       command=lambda: set_linecolor("yellow"))
orangeLine = tk.Button(dataFrame, bg="orange", activebackground="orange",
                       command=lambda: set_linecolor("orange"))
redLine = tk.Button(dataFrame, bg="red", activebackground="red",
                    command=lambda: set_linecolor("red"))
purpleLine = tk.Button(dataFrame, bg="purple", activebackground="purple",
                       command=lambda: set_linecolor("purple"))
greenLine = tk.Button(dataFrame, bg="green", activebackground="green",
                      command=lambda: set_linecolor("green"))
darkGreenLine = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                          command=lambda: set_linecolor("darkgreen"))
lightBlueLine = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                          command=lambda: set_linecolor("lightblue"))

lineColorBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text='Выбрать другой цвет от-ка',
                         font=("Consolas", 12), command=get_color_line)

yColorLine = 1.2
lineColorLabel.place(x=5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                     height=DATA_FRAME_HEIGHT // COLUMNS)

whiteLine.place(x=DATA_FRAME_WIGHT // 2.5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowLine.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeLine.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redLine.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
              height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleLine.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenLine.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenLine.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueLine.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)

lineColorBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColorLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                   width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColorTextLabel.place(x=0, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                            height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColorLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                        width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)


clipperColorLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет отсекателя:",
                             font=("Consolas", 13),
                             fg=MAIN_COLOR_LABEL_TEXT)

clipperCurColorTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет отсекателя:",
                                    font=("Consolas", 13),
                                    fg=MAIN_COLOR_LABEL_TEXT)

clipperCurColorLabel = tk.Label(dataFrame, bg=CLIPPER_COLOR)


def get_color_clipper():
    color_code = colorchooser.askcolor(title="Choose color clipper")
    set_clippercolor(color_code[-1])


def set_clippercolor(color):
    global CLIPPER_COLOR
    CLIPPER_COLOR = color
    clipperCurColorLabel.configure(bg=CLIPPER_COLOR)


whiteClipper = tk.Button(dataFrame, bg="white", activebackground="white",
                         command=lambda: set_clippercolor("white"))
yellowClipper = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                          command=lambda: set_clippercolor("yellow"))
orangeClipper = tk.Button(dataFrame, bg="orange", activebackground="orange",
                          command=lambda: set_clippercolor("orange"))
redClipper = tk.Button(dataFrame, bg="red", activebackground="red",
                       command=lambda: set_clippercolor("red"))
purpleClipper = tk.Button(dataFrame, bg="purple", activebackground="purple",
                          command=lambda: set_clippercolor("purple"))
greenClipper = tk.Button(dataFrame, bg="green", activebackground="green",
                         command=lambda: set_clippercolor("green"))
darkGreenClipper = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                             command=lambda: set_clippercolor("darkgreen"))
lightBlueClipper = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                             command=lambda: set_clippercolor("lightblue"))

clipperColorBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text='Выбрать другой цвет от-ля',
                            font=("Consolas", 12), command=get_color_clipper)

yColorLine += 3
clipperColorLabel.place(x=5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                        height=DATA_FRAME_HEIGHT // COLUMNS)

whiteClipper.place(x=DATA_FRAME_WIGHT // 2.5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowClipper.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                       height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                       height=DATA_FRAME_HEIGHT // COLUMNS - 10)

clipperColorBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColorLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                      width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
clipperCurColorTextLabel.place(x=0, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                               height=DATA_FRAME_HEIGHT // COLUMNS)
clipperCurColorLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                           width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

resultColorLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет результата:",
                            font=("Consolas", 13),
                            fg=MAIN_COLOR_LABEL_TEXT)

resultCurColorTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет результата:",
                                   font=("Consolas", 13),
                                   fg=MAIN_COLOR_LABEL_TEXT)


def get_color_result():
    color_code = colorchooser.askcolor(title="Choose color result")
    set_resultcolor(color_code[-1])


def set_resultcolor(color):
    global RESULT_COLOR
    RESULT_COLOR = color
    resultCurColorLabel.configure(bg=RESULT_COLOR)


resultCurColorLabel = tk.Label(dataFrame, bg=RESULT_COLOR)

whiteResult = tk.Button(dataFrame, bg="white", activebackground="white",
                        command=lambda: set_resultcolor("white"))
yellowResult = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                         command=lambda: set_resultcolor("yellow"))
orangeResult = tk.Button(dataFrame, bg="orange", activebackground="orange",
                         command=lambda: set_resultcolor("orange"))
redResult = tk.Button(dataFrame, bg="red", activebackground="red",
                      command=lambda: set_resultcolor("red"))
purpleResult = tk.Button(dataFrame, bg="purple", activebackground="purple",
                         command=lambda: set_resultcolor("purple"))
greenResult = tk.Button(dataFrame, bg="green", activebackground="green",
                        command=lambda: set_resultcolor("green"))
darkGreenResult = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                            command=lambda: set_resultcolor("darkgreen"))
lightBlueResult = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                            command=lambda: set_resultcolor("lightblue"))

resultColorBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text='Выбрать другой цвет рез-та',
                           font=("Consolas", 12), command=get_color_result)

yColorLine += 3
resultColorLabel.place(x=5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                       height=DATA_FRAME_HEIGHT // COLUMNS)

whiteResult.place(x=DATA_FRAME_WIGHT // 2.5, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                  height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowResult.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeResult.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redResult.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleResult.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenResult.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                  height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenResult.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                      height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueResult.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColorLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                      height=DATA_FRAME_HEIGHT // COLUMNS - 10)

resultColorBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColorLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                     width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
resultCurColorTextLabel.place(x=0, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                              height=DATA_FRAME_HEIGHT // COLUMNS)
resultCurColorLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColorLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                          width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение точки

pointMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOR_LABEL_BG, text="ПОСТРОЕНИЕ ОТРЕЗКА",
                          font=("Consolas", 14),
                          fg=MAIN_COLOR_LABEL_TEXT, relief=tk.SOLID)

msgAboutPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Xн        Yн       Xк        Yк",
                         font=("Consolas", 14),
                         fg=MAIN_COLOR_LABEL_TEXT)

xnEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
ynEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
xkEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
ykEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")

drawLineBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Построить отрезок",
                        font=("Consolas", 12), command=draw_line)


makePoint = yColorLine + 3.1
pointMakeLabel.place(x=0, y=makePoint * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                     height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutPoint.place(x=0, y=(makePoint + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                    height=DATA_FRAME_HEIGHT // COLUMNS)

xnEntry.place(x=5,                         y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS,
              width=DATA_FRAME_WIGHT // 4 - 5, height=DATA_FRAME_HEIGHT // COLUMNS)
ynEntry.place(x=1 * DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS,
              width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
xkEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS,
              width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
ykEntry.place(x=3 * DATA_FRAME_WIGHT // 4, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS,
              width=DATA_FRAME_WIGHT // 4 - 5, height=DATA_FRAME_HEIGHT // COLUMNS)

makePoint += 0.2
drawLineBtn.place(x=DATA_FRAME_WIGHT // 6, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS,
                  width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение точки

clipperMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOR_LABEL_BG, text="ПОСТРОЕНИЕ ОТСЕКАТЕЛЯ",
                            font=("Consolas", 14),
                            fg=MAIN_COLOR_LABEL_TEXT, relief=tk.SOLID)

msgAboutClipper = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="X\t\tY",
                           font=("Consolas", 14),
                           fg=MAIN_COLOR_LABEL_TEXT)

xclEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
yclEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")

drawClipperVertexBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Построить вершину",
                                 font=("Consolas", 12), command=draw_vertex)
drawClipperCloseBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Замкнуть",
                                font=("Consolas", 12), command=click_middle)

makeClipper = makePoint + 4.1
clipperMakeLabel.place(x=0, y=makeClipper * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutClipper.place(x=0, y=(makeClipper + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)

xclEntry.place(x=10,                         y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
yclEntry.place(x=1 * DATA_FRAME_WIGHT // 2, y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)

makeClipper += 0.2
drawClipperVertexBtn.place(x=10, y=(makeClipper + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10,
                           height=DATA_FRAME_HEIGHT // COLUMNS)
drawClipperCloseBtn.place(x=DATA_FRAME_WIGHT // 2, y=(makeClipper + 3) * DATA_FRAME_HEIGHT // COLUMNS,
                          width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
modeByMouse = tk.Label(dataFrame, bg=MAIN_COLOR_LABEL_BG, text="ПОСТРОЕНИЕ с помощью мыши",
                       font=("Consolas", 14),
                       fg=MAIN_COLOR_LABEL_TEXT, relief=tk.SOLID)
labelTextInfo_1 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Левая кнопка - Добавить вершину отсекатель",
                           font=("Consolas", 12),
                           fg=MAIN_COLOR_LABEL_TEXT)
labelTextInfo_2 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Средная кнопка - Замкнуть отсекатель",
                           font=("Consolas", 12),
                           fg=MAIN_COLOR_LABEL_TEXT)
labelTextInfo_3 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Правая кнопка - Добавить отрезок",
                           font=("Consolas", 12),
                           fg=MAIN_COLOR_LABEL_TEXT)
modeMouse = makeClipper + 4 + 0.2
modeByMouse.place(x=0, y=modeMouse * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                  height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_1.place(x=0, y=(modeMouse + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_2.place(x=0, y=(modeMouse + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_3.place(x=0, y=(modeMouse + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Кнопки сравнения, очистки


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CANVAS FILED FOR DRAWING lines and spectres by algorithms
currentFigure = []
allFigures = []

canvasField = tk.Canvas(root, bg=CANVAS_COLOR, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvasField.pack(side=tk.RIGHT, padx=BORDERS_SPACE)

canvasField.bind("<Button-1>", lambda event: click_left(event))
canvasField.bind("<Button-2>", lambda event: click_middle())
canvasField.bind("<Button-3>", lambda event: click_right(event, lines, canvasField, LINE_COLOR))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


cutBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Отсечь", font=("Consolas", 12),
                   command=cut_off_command)
ParallelLinesBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT,
                             text="Построить параллельные отрезки", font=("Consolas", 12), command=add_parallel_lines)
clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Очистить экран",
                           font=("Consolas", 12), command=clear_canvas)

ParallelLinesBtn.place(x=40, y=(modeMouse + 4) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
cutBtn.place(x=40, y=(modeMouse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
             height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(modeMouse + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
                     height=DATA_FRAME_HEIGHT // COLUMNS)

xnEntry.insert(0, 100)
ynEntry.insert(0, 200)
xkEntry.insert(0, 800)
ykEntry.insert(0, 500)

xclEntry.insert(0, 200)
yclEntry.insert(0, 100)


root.mainloop()
