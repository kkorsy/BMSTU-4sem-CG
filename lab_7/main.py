import tkinter as tk
from tkinter import colorchooser, messagebox

from config import *
from draw import add_line, draw_rectangle, click_right, draw_rectangle_by_button
from algorithm import mid_point_algorithm

root = tk.Tk()
root.title("КГ Лабораторная работа №7")
root["bg"] = MAIN_COLOUR
root.state('zoomed')

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)

lines = []
rectangle = [-1, -1, -1, -1]
is_set_rectangle = False


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
def click_left_motion(event):
    global is_set_rectangle
    is_set_rectangle = draw_rectangle_by_button(event, rectangle, lines, canvasField, CLIPPER_COLOUR, is_set_rectangle)


def cut_off_command():
    if rectangle[0] == -1:
        messagebox.showinfo("Ошибка", "Отсутствует отсекатель")

    rect = [min(rectangle[0], rectangle[2]), max(rectangle[0], rectangle[2]),
            min(rectangle[1], rectangle[3]), max(rectangle[1], rectangle[3])]

    canvasField.create_rectangle(rect[0] + 1, rect[2] + 1, rect[1] - 1, rect[3] - 1,
                                 fill=CANVAS_COLOUR, outline=CANVAS_COLOUR)

    for line in lines:
        if line:
            n_line = mid_point_algorithm(rect, line)
            if len(n_line) != 0:
                canvasField.create_line(n_line[0][0], n_line[0][1], n_line[1][0], n_line[1][1], fill=RESULT_COLOUR)


def clear_canvas():
    global is_set_rectangle
    canvasField.delete("all")
    lines.clear()
    is_set_rectangle = False
    for i in range(4):
        rectangle[i] = -1


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

        add_line(canvasField, lines, x_start, y_start, x_end, y_end, LINE_COLOUR)


def add_vert_horiz_lines(rect, line_list, canvas, colour):
    if rect[0] == -1:
        messagebox.showerror("Ошибка", "Отсутствует отсекатель")
        return

    x1 = rect[0]
    y1 = rect[1]
    x2 = rect[2]
    y2 = rect[3]

    dy = y2 - y1
    dx = x2 - x1

    line_list.append([[x1, y1 + 0.1 * dy], [x1, y2 - 0.1 * dy], colour])
    line_list.append([[x1 + 0.1 * dx, y1], [x2 - 0.1 * dx, y1], colour])

    canvas.create_line(x1, y1 + 0.1 * dy, x1, y2 - 0.1 * dy, fill=colour)
    canvas.create_line(x1 + 0.1 * dx, y1, x2 - 0.1 * dx, y1, fill=colour)


def draw_clipper():
    try:
        xl = int(xlbEntry.get())
        yl = int(ylbEntry.get())
        xr = int(xrlEntry.get())
        yr = int(yrlEntry.get())
    except TypeError:
        messagebox.showwarning("Ошибка ввода",
                               "Неверно заданны координаты вершин прямоугольника!\n"
                               "Ожидался ввод целых чисел.")
        return

    rectangle[0] = xl
    rectangle[1] = yl
    rectangle[2] = xr
    rectangle[3] = yr

    draw_rectangle(canvasField, rectangle, lines, CLIPPER_COLOUR)


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# INPUT DATA FRAME
dataFrame = tk.Frame(root, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT)
dataFrame["bg"] = MAIN_FRAME_COLOR

dataFrame.pack(side=tk.LEFT, padx=BORDERS_SPACE, fill=tk.Y)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# ВЫБОР цвета

chooseColourMainLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ВЫБОР ЦВЕТА",
                                 font=("Consolas", 14), fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

size = (DATA_FRAME_WIGHT // 1.7) // 8
chooseColourMainLabel.place(x=0, y=0, width=DATA_FRAME_WIGHT, height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# выбор цвета отрезка

lineColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет отрезка:",
                           font=("Consolas", 14),
                           fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет отрезка:",
                                  font=("Consolas", 13),
                                  fg=MAIN_COLOUR_LABEL_TEXT)

lineCurColourLabel = tk.Label(dataFrame, bg="black")


def get_colour_line():
    color_code = colorchooser.askcolor(title="Choose colour line")
    set_linecolor(color_code[-1])


def set_linecolor(color):
    global LINE_COLOUR
    LINE_COLOUR = color
    lineCurColourLabel.configure(bg=LINE_COLOUR)


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

lineColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать другой цвет от-ка',
                          font=("Consolas", 12), command=get_colour_line)

yColourLine = 1.2
lineColourLabel.place(x=5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                      height=DATA_FRAME_HEIGHT // COLUMNS)

whiteLine.place(x=DATA_FRAME_WIGHT // 2.5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowLine.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeLine.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redLine.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
              height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleLine.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenLine.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenLine.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueLine.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)

lineColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                    width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourTextLabel.place(x=0, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                             height=DATA_FRAME_HEIGHT // COLUMNS)
lineCurColourLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                         width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)


clipperColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет отсекателя:",
                              font=("Consolas", 13),
                              fg=MAIN_COLOUR_LABEL_TEXT)

clipperCurColourTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет отсекателя:",
                                     font=("Consolas", 13),
                                     fg=MAIN_COLOUR_LABEL_TEXT)

clipperCurColourLabel = tk.Label(dataFrame, bg=CLIPPER_COLOUR)


def get_colour_clipper():
    color_code = colorchooser.askcolor(title="Choose colour clipper")
    set_clippercolor(color_code[-1])


def set_clippercolor(color):
    global CLIPPER_COLOUR
    CLIPPER_COLOUR = color
    clipperCurColourLabel.configure(bg=CLIPPER_COLOUR)


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

clipperColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать другой цвет от-ля',
                             font=("Consolas", 12), command=get_colour_clipper)

yColourLine += 3
clipperColourLabel.place(x=5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                         height=DATA_FRAME_HEIGHT // COLUMNS)

whiteClipper.place(x=DATA_FRAME_WIGHT // 2.5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowClipper.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                 height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                    height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                       height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueClipper.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                       height=DATA_FRAME_HEIGHT // COLUMNS - 10)

clipperColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                       width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
clipperCurColourTextLabel.place(x=0, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                                height=DATA_FRAME_HEIGHT // COLUMNS)
clipperCurColourLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                            width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

resultColourLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет результата:",
                             font=("Consolas", 13),
                             fg=MAIN_COLOUR_LABEL_TEXT)

resultCurColourTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет результата:",
                                    font=("Consolas", 13),
                                    fg=MAIN_COLOUR_LABEL_TEXT)


def get_colour_result():
    color_code = colorchooser.askcolor(title="Choose colour result")
    set_resultcolor(color_code[-1])


def set_resultcolor(color):
    global RESULT_COLOUR
    RESULT_COLOUR = color
    resultCurColourLabel.configure(bg=RESULT_COLOUR)


resultCurColourLabel = tk.Label(dataFrame, bg=RESULT_COLOUR)
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

resultColourBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text='Выбрать другой цвет рез-та',
                            font=("Consolas", 12), command=get_colour_result)

yColourLine += 3
resultColourLabel.place(x=5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2.5,
                        height=DATA_FRAME_HEIGHT // COLUMNS)

whiteResult.place(x=DATA_FRAME_WIGHT // 2.5, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                  height=DATA_FRAME_HEIGHT // COLUMNS - 10)
yellowResult.place(x=DATA_FRAME_WIGHT // 2.5 + size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
orangeResult.place(x=DATA_FRAME_WIGHT // 2.5 + 2 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
redResult.place(x=DATA_FRAME_WIGHT // 2.5 + 3 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                height=DATA_FRAME_HEIGHT // COLUMNS - 10)
purpleResult.place(x=DATA_FRAME_WIGHT // 2.5 + 4 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                   height=DATA_FRAME_HEIGHT // COLUMNS - 10)
greenResult.place(x=DATA_FRAME_WIGHT // 2.5 + 5 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                  height=DATA_FRAME_HEIGHT // COLUMNS - 10)
darkGreenResult.place(x=DATA_FRAME_WIGHT // 2.5 + 6 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                      height=DATA_FRAME_HEIGHT // COLUMNS - 10)
lightBlueResult.place(x=DATA_FRAME_WIGHT // 2.5 + 7 * size, y=yColourLine * DATA_FRAME_HEIGHT // COLUMNS, width=size,
                      height=DATA_FRAME_HEIGHT // COLUMNS - 10)

resultColourBtn.place(x=DATA_FRAME_WIGHT // 3 - BORDERS_SPACE, y=(yColourLine + 1) * DATA_FRAME_HEIGHT // COLUMNS,
                      width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)
resultCurColourTextLabel.place(x=0, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 1.5,
                               height=DATA_FRAME_HEIGHT // COLUMNS)
resultCurColourLabel.place(x=DATA_FRAME_WIGHT // 1.5, y=(yColourLine + 2) * DATA_FRAME_HEIGHT // COLUMNS + 5,
                           width=DATA_FRAME_WIGHT // 8, height=DATA_FRAME_HEIGHT // COLUMNS - 10)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Построение точки

pointMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ ОТРЕЗКА",
                          font=("Consolas", 14),
                          fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

msgAboutPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Xн        Yн       Xк        Yк",
                         font=("Consolas", 14),
                         fg=MAIN_COLOUR_LABEL_TEXT)

xnEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
ynEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
xkEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
ykEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")

drawLineBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить отрезок",
                        font=("Consolas", 12), command=draw_line)


makePoint = yColourLine + 3.1
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

clipperMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ ОТСЕКАТЕЛЯ",
                            font=("Consolas", 14),
                            fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)

msgAboutClipper = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Xлв       Yлв      Xпн        Yпн",
                           font=("Consolas", 14),
                           fg=MAIN_COLOUR_LABEL_TEXT)

xlbEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
ylbEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
xrlEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")
yrlEntry = tk.Entry(dataFrame, bg=MAIN_COLOUR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR, justify="center")

drawClipperBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Построить отсекатель",
                           font=("Consolas", 12), command=draw_clipper)


makeClipper = makePoint + 4.1
clipperMakeLabel.place(x=0, y=makeClipper * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutClipper.place(x=0, y=(makeClipper + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)

xlbEntry.place(x=5,                         y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 4 - 5, height=DATA_FRAME_HEIGHT // COLUMNS)
ylbEntry.place(x=1 * DATA_FRAME_WIGHT // 4, y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
xrlEntry.place(x=2 * DATA_FRAME_WIGHT // 4, y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 4, height=DATA_FRAME_HEIGHT // COLUMNS)
yrlEntry.place(x=3 * DATA_FRAME_WIGHT // 4, y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS,
               width=DATA_FRAME_WIGHT // 4 - 5, height=DATA_FRAME_HEIGHT // COLUMNS)

makeClipper += 0.2
drawClipperBtn.place(x=DATA_FRAME_WIGHT // 6, y=(makeClipper + 3) * DATA_FRAME_HEIGHT // COLUMNS,
                     width=DATA_FRAME_WIGHT // 1.5, height=DATA_FRAME_HEIGHT // COLUMNS)

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
modeByMouse = tk.Label(dataFrame, bg=MAIN_COLOUR_LABEL_BG, text="ПОСТРОЕНИЕ с помощью мыши",
                       font=("Consolas", 14),
                       fg=MAIN_COLOUR_LABEL_TEXT, relief=tk.SOLID)
labelTextInfo_1 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Правая кнопка - Добавить отрезок",
                           font=("Consolas", 12),
                           fg=MAIN_COLOUR_LABEL_TEXT)
labelTextInfo_2 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Левая кнопка - Добавить отсекатель \n(прямоугольник)",
                           font=("Consolas", 12),
                           fg=MAIN_COLOUR_LABEL_TEXT)
modeMouse = makeClipper + 4 + 0.2
modeByMouse.place(x=0, y=modeMouse * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                  height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_1.place(x=0, y=(modeMouse + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)
labelTextInfo_2.place(x=0, y=(modeMouse + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Кнопки сравнения, очистки


# ------------------------------------------------------------------------------------------------------------------------------------------------------------------
# CANVAS FILED FOR DRAWING lines and spectres by algorithms
currentFigure = []
allFigures = []

canvasField = tk.Canvas(root, bg=CANVAS_COLOUR, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvasField.pack(side=tk.RIGHT, padx=BORDERS_SPACE)

canvasField.bind("<Button-3>", lambda event: click_right(event, lines, canvasField, LINE_COLOUR))
canvasField.bind("<B1-Motion>", lambda event: click_left_motion(event))
# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


addLineBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT,
                       text="Добавить горизонтальные и \nвертикальные отрезки", font=("Consolas", 12),
                       command=lambda: add_vert_horiz_lines(rectangle, lines, canvasField, LINE_COLOUR))
cutBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Отсечь", font=("Consolas", 12),
                   command=cut_off_command)

clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOUR, fg=MAIN_COLOUR_LABEL_TEXT, text="Очистить экран",
                           font=("Consolas", 12), command=clear_canvas)

addLineBtn.place(x=40, y=(modeMouse + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
                 height=2 * DATA_FRAME_HEIGHT // COLUMNS)
cutBtn.place(x=40, y=(modeMouse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
             height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(modeMouse + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
                     height=DATA_FRAME_HEIGHT // COLUMNS)

xnEntry.insert(0, 100)
ynEntry.insert(0, 200)
xkEntry.insert(0, 800)
ykEntry.insert(0, 500)

xlbEntry.insert(0, 200)
ylbEntry.insert(0, 100)

xrlEntry.insert(0, 700)
yrlEntry.insert(0, 600)

root.mainloop()
