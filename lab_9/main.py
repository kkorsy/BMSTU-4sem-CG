import tkinter as tk
from tkinter import colorchooser

from config import *
from command import clear_canvas, click_btn, close_figure, add_vertex, cut_off

root = tk.Tk()
root.title("КГ Лабораторная работа №9 \"Алгоритм Сазерленда-Ходжмена\"")
root["bg"] = MAIN_COLOR
root.state('zoomed')

root.geometry(str(WINDOW_WIDTH) + "x" + str(WINDOW_HEIGHT))
root.resizable(height=False, width=False)

figure = []
clipper = []

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

lineColorLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Цвет фигуры:",
                          font=("Consolas", 14),
                          fg=MAIN_COLOR_LABEL_TEXT)

lineCurColorTextLabel = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Текущий цвет фигуры:",
                                 font=("Consolas", 13),
                                 fg=MAIN_COLOR_LABEL_TEXT)

lineCurColorLabel = tk.Label(dataFrame, bg="black")


def get_color_line():
    color_code = colorchooser.askcolor(title="Choose color line")
    set_color_line(color_code[-1])


def set_color_line(color):
    global FIGURE_COLOR
    FIGURE_COLOR = color
    lineCurColorLabel.configure(bg=FIGURE_COLOR)


whiteLine = tk.Button(dataFrame, bg="white", activebackground="white",
                      command=lambda: set_color_line("white"))
yellowLine = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                       command=lambda: set_color_line("yellow"))
orangeLine = tk.Button(dataFrame, bg="orange", activebackground="orange",
                       command=lambda: set_color_line("orange"))
redLine = tk.Button(dataFrame, bg="red", activebackground="red",
                    command=lambda: set_color_line("red"))
purpleLine = tk.Button(dataFrame, bg="purple", activebackground="purple",
                       command=lambda: set_color_line("purple"))
greenLine = tk.Button(dataFrame, bg="green", activebackground="green",
                      command=lambda: set_color_line("green"))
darkGreenLine = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                          command=lambda: set_color_line("darkgreen"))
lightBlueLine = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                          command=lambda: set_color_line("lightblue"))

lineColorBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text='Выбрать другой цвет фигуры',
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
    set_color_clipper(color_code[-1])


def set_color_clipper(color):
    global CLIPPER_COLOR
    CLIPPER_COLOR = color
    clipperCurColorLabel.configure(bg=CLIPPER_COLOR)


whiteClipper = tk.Button(dataFrame, bg="white", activebackground="white",
                         command=lambda: set_color_clipper("white"))
yellowClipper = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                          command=lambda: set_color_clipper("yellow"))
orangeClipper = tk.Button(dataFrame, bg="orange", activebackground="orange",
                          command=lambda: set_color_clipper("orange"))
redClipper = tk.Button(dataFrame, bg="red", activebackground="red",
                       command=lambda: set_color_clipper("red"))
purpleClipper = tk.Button(dataFrame, bg="purple", activebackground="purple",
                          command=lambda: set_color_clipper("purple"))
greenClipper = tk.Button(dataFrame, bg="green", activebackground="green",
                         command=lambda: set_color_clipper("green"))
darkGreenClipper = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                             command=lambda: set_color_clipper("darkgreen"))
lightBlueClipper = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                             command=lambda: set_color_clipper("lightblue"))

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
    set_color_result(color_code[-1])


def set_color_result(color):
    global RESULT_COLOR
    RESULT_COLOR = color
    resultCurColorLabel.configure(bg=RESULT_COLOR)


resultCurColorLabel = tk.Label(dataFrame, bg=RESULT_COLOR)

whiteResult = tk.Button(dataFrame, bg="white", activebackground="white",
                        command=lambda: set_color_result("white"))
yellowResult = tk.Button(dataFrame, bg="yellow", activebackground="yellow",
                         command=lambda: set_color_result("yellow"))
orangeResult = tk.Button(dataFrame, bg="orange", activebackground="orange",
                         command=lambda: set_color_result("orange"))
redResult = tk.Button(dataFrame, bg="red", activebackground="red",
                      command=lambda: set_color_result("red"))
purpleResult = tk.Button(dataFrame, bg="purple", activebackground="purple",
                         command=lambda: set_color_result("purple"))
greenResult = tk.Button(dataFrame, bg="green", activebackground="green",
                        command=lambda: set_color_result("green"))
darkGreenResult = tk.Button(dataFrame, bg="darkgreen", activebackground="darkgreen",
                            command=lambda: set_color_result("darkgreen"))
lightBlueResult = tk.Button(dataFrame, bg="lightblue", activebackground="lightblue",
                            command=lambda: set_color_result("lightblue"))

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

pointMakeLabel = tk.Label(dataFrame, bg=MAIN_COLOR_LABEL_BG, text="ПОСТРОЕНИЕ ФИГУРЫ",
                          font=("Consolas", 14),
                          fg=MAIN_COLOR_LABEL_TEXT, relief=tk.SOLID)

msgAboutPoint = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="X\t\tY",
                         font=("Consolas", 14),
                         fg=MAIN_COLOR_LABEL_TEXT)

xFigureEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR,
                        justify="center")
yFigureEntry = tk.Entry(dataFrame, bg=MAIN_COLOR_LABEL_TEXT, font=("Consolas", 12), fg=MAIN_FRAME_COLOR,
                        justify="center")

drawFigureVertexBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Построить вершину",
                                font=("Consolas", 12),
                                command=lambda: add_vertex(canvasField, clipper, figure, CLIPPER_COLOR, FIGURE_COLOR,
                                                           xFigureEntry, yFigureEntry))
drawFigureCloseBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Замкнуть фигуру",
                               font=("Consolas", 12),
                               command=lambda: close_figure(canvasField, figure, FIGURE_COLOR,
                                                            "Отсекаемый многоугольник"))

makePoint = yColorLine + 3.1
pointMakeLabel.place(x=0, y=makePoint * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                     height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutPoint.place(x=0, y=(makePoint + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                    height=DATA_FRAME_HEIGHT // COLUMNS)

xFigureEntry.place(x=10, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10,
                   height=DATA_FRAME_HEIGHT // COLUMNS)
yFigureEntry.place(x=DATA_FRAME_WIGHT // 2, y=(makePoint + 2) * DATA_FRAME_HEIGHT // COLUMNS,
                   width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)

makePoint += 0.2
drawFigureVertexBtn.place(x=10, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10,
                          height=DATA_FRAME_HEIGHT // COLUMNS)
drawFigureCloseBtn.place(x=DATA_FRAME_WIGHT // 2, y=(makePoint + 3) * DATA_FRAME_HEIGHT // COLUMNS,
                         width=DATA_FRAME_WIGHT // 2 - 10, height=DATA_FRAME_HEIGHT // COLUMNS)

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
                                 font=("Consolas", 12),
                                 command=lambda: add_vertex(canvasField, figure, clipper, FIGURE_COLOR, CLIPPER_COLOR,
                                                            xclEntry, yclEntry))
drawClipperCloseBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Замкнуть от-ль",
                                font=("Consolas", 12),
                                command=lambda: close_figure(canvasField, clipper, CLIPPER_COLOR, "Отсекатель"))

makeClipper = makePoint + 4.1
clipperMakeLabel.place(x=0, y=makeClipper * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                       height=DATA_FRAME_HEIGHT // COLUMNS)
msgAboutClipper.place(x=0, y=(makeClipper + 1) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT,
                      height=DATA_FRAME_HEIGHT // COLUMNS)

xclEntry.place(x=10, y=(makeClipper + 2) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT // 2 - 10,
               height=DATA_FRAME_HEIGHT // COLUMNS)
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
labelTextInfo_2 = tk.Label(dataFrame, bg=MAIN_FRAME_COLOR, text="Правая кнопка - Добавить вершины фигуры",
                           font=("Consolas", 12),
                           fg=MAIN_COLOR_LABEL_TEXT)
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

canvasField = tk.Canvas(root, bg=CANVAS_COLOR, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
canvasField.pack(side=tk.RIGHT, padx=BORDERS_SPACE)

canvasField.bind("<Button-1>",
                 lambda event: click_btn(event, figure, clipper, canvasField, CLIPPER_COLOR, FIGURE_COLOR))
canvasField.bind("<Button-3>",
                 lambda event: click_btn(event, clipper, figure, canvasField, FIGURE_COLOR, CLIPPER_COLOR))

# ------------------------------------------------------------------------------------------------------------------------------------------------------------------


cutBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Отсечь", font=("Consolas", 12),
                   command=lambda: cut_off(canvasField, figure, clipper, RESULT_COLOR))
clearCanvasBtn = tk.Button(dataFrame, bg=MAIN_COLOR, fg=MAIN_COLOR_LABEL_TEXT, text="Очистить экран",
                           font=("Consolas", 12), command=lambda: clear_canvas(canvasField, figure, clipper))

cutBtn.place(x=40, y=(modeMouse + 5) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
             height=DATA_FRAME_HEIGHT // COLUMNS)
clearCanvasBtn.place(x=40, y=(modeMouse + 6) * DATA_FRAME_HEIGHT // COLUMNS, width=DATA_FRAME_WIGHT - 80,
                     height=DATA_FRAME_HEIGHT // COLUMNS)

xFigureEntry.insert(0, 100)
yFigureEntry.insert(0, 200)

xclEntry.insert(0, 200)
yclEntry.insert(0, 100)

root.mainloop()
