from PyQt5 import QtWidgets, uic
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap
from PyQt5.QtCore import Qt
from math import sqrt, pi, cos, sin
import time
from matplotlib import pyplot as plt
import numpy as np


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)

        uic.loadUi("window.ui", self)
        self.scene = QtWidgets.QGraphicsScene(0, 0, 611, 611)
        self.mainview.setScene(self.scene)
        self.mainview.setFixedWidth(620)
        self.mainview.setFixedHeight(620)

        self.image = QImage(611, 611, QImage.Format_ARGB32_Premultiplied)
        self.pen = QPen()
        self.color_line = QColor(Qt.black)
        self.color_bground = QColor(Qt.white)
        self.draw_once.clicked.connect(lambda: draw_once(self))
        self.clean_all.clicked.connect(lambda: clear_all(self))
        self.btn_bground.clicked.connect(lambda: get_color_bground(self))
        self.btn_line.clicked.connect(lambda: get_color_line(self))
        self.draw_centr.clicked.connect(lambda: draw_spectrum(self))
        self.btn_time.clicked.connect(lambda: time_measure(self))
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.what)
        layout.addWidget(self.other)
        self.setLayout(layout)
        self.circle.setChecked(True)
        self.canon.setChecked(True)


def time_measure(win):
    number_of_runs = 100

    max_r = 100
    step = 10

    r_list = np.arange(step, max_r + step, step)
    circle_time_canon = [0] * len(r_list)
    circle_time_param = [0] * len(r_list)
    circle_time_brez = [0] * len(r_list)
    circle_time_middle = [0] * len(r_list)

    for r in range(len(r_list)):
        for i in range(number_of_runs):
            t1 = time.time()
            ellips_canon(win, 305, 305, r_list[r], r_list[r])
            t2 = time.time()
            circle_time_canon[r] += t2 - t1

            t1 = time.time()
            ellips_param(win, 305, 305, r_list[r], r_list[r])
            t2 = time.time()
            circle_time_param[r] += t2 - t1

            t1 = time.time()
            ellips_brez(win, 305, 305, r_list[r], r_list[r])
            t2 = time.time()
            circle_time_brez[r] += t2 - t1

            t1 = time.time()
            ellips_middle(win, 305, 305, r_list[r], r_list[r])
            t2 = time.time()
            circle_time_middle[r] += t2 - t1

            clear_all(win)
        circle_time_canon[r] /= number_of_runs
        circle_time_param[r] /= number_of_runs
        circle_time_brez[r] /= number_of_runs
        circle_time_middle[r] /= number_of_runs

    plt.subplot(2, 1, 1)
    plt.rcParams['font.size'] = '12'
    plt.title("Замеры времени для построения окружности\n")

    plt.plot(r_list, circle_time_canon, label='Каноническое уравнение')
    plt.plot(r_list, circle_time_param, label='Параметрическое уравнение')
    plt.plot(r_list, circle_time_middle, label='Алгоритм средней точки')
    plt.plot(r_list, circle_time_brez, label='Алгоритм Брезенхема')

    plt.xticks(np.arange(step, max_r + step, step))
    plt.legend()
    plt.xlabel("R")
    plt.ylabel("t")

    a = round(step / 2)
    max_b = 100
    step = 10

    b_list = np.arange(step, max_b + step, step)
    ellips_time_canon = [0] * len(b_list)
    ellips_time_param = [0] * len(b_list)
    ellips_time_brez = [0] * len(b_list)
    ellips_time_middle = [0] * len(b_list)

    for r in range(len(b_list)):
        for i in range(number_of_runs):
            t1 = time.time()
            ellips_canon(win, 305, 305, a, b_list[r])
            t2 = time.time()
            ellips_time_canon[r] += t2 - t1

            t1 = time.time()
            ellips_param(win, 305, 305, a, r_list[r])
            t2 = time.time()
            ellips_time_param[r] += t2 - t1

            t1 = time.time()
            ellips_brez(win, 305, 305, a, r_list[r])
            t2 = time.time()
            ellips_time_brez[r] += t2 - t1

            t1 = time.time()
            ellips_middle(win, 305, 305, a, r_list[r])
            t2 = time.time()
            ellips_time_middle[r] += t2 - t1

            clear_all(win)
        a += step

        ellips_time_canon[r] /= number_of_runs
        ellips_time_param[r] /= number_of_runs
        ellips_time_brez[r] /= number_of_runs
        ellips_time_middle[r] /= number_of_runs

    plt.subplot(2, 1, 2)
    plt.tight_layout()
    plt.rcParams['font.size'] = '12'
    plt.title("Замеры времени для построения эллипса\n")

    plt.plot(b_list, ellips_time_canon, label='Каноническое уравнение')
    plt.plot(b_list, ellips_time_param, label='Параметрическое уравнение')
    plt.plot(b_list, ellips_time_middle, label='Алгоритм средней точки')
    plt.plot(b_list, ellips_time_brez, label='Алгоритм Брезенхема')

    plt.xticks(np.arange(step, max_r + step, step))
    plt.legend()
    plt.xlabel("b")
    plt.ylabel("t")

    fig_manager = plt.get_current_fig_manager()
    fig_manager.window.showMaximized()
    plt.show()


def circle_canon(win, cx, cy, r):
    # (x - x0)^2 + (y - y0)^2 = R^2
    k = round(r / sqrt(2))
    for x in range(0, k + 1, 1):
        y = round(sqrt(r ** 2 - x ** 2))
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())


def circle_param(win, cx, cy, r):
    # x = x0 + R * cost
    # y = y0 + R * sint
    k = round(pi * r / 4)  # длина 1/8 окружности
    for i in range(0, k + 1, 1):
        x = round(r * cos(i / r))
        y = round(r * sin(i / r))
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())


def circle_brez(win, cx, cy, r):
    x = 0   # задание начальных значений
    y = r
    d = 2 * (1 - r)
    while y >= x:
        # высвечивание текущего пиксела
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())

        if d < 0:  # пиксель лежит внутри окружности
            buf = 2 * d + 2 * y - 1
            x += 1

            if buf <= 0:  # горизонтальный шаг
                d = d + 2 * x + 1
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * (x - y + 1)
        elif d > 0:  # пиксель лежит вне окружности
            buf = 2 * d - 2 * x - 1
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y + 1
            else:  # диагональный шаг
                x += 1
                d = d + 2 * (x - y + 1)
        elif d == 0.0:  # пиксель лежит на окружности
            x += 1   # диагональный шаг
            y -= 1
            d = d + 2 * (x - y + 1)


def circle_middle(win, cx, cy, r):
    x = 0  # начальные значения
    y = r
    p = 5 / 4 - r  # (x + 1)^2 + (y - 1/2)^2 - r^2
    while x <= y:
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        win.image.setPixel(cx - y, cy + x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx - y, cy - x, win.pen.color().rgb())
        win.image.setPixel(cx + y, cy + x, win.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри окружности, ближе верхний пиксел, горизонтальный шаг
            p += 2 * x + 1
        else:   # средняя точка вне окружности, ближе диагональный пиксел, диагональный шаг
            y -= 1
            p += 2 * (x - y) + 1


def ellips_canon(win, cx, cy, a, b):
    for x in range(0, a + 1, 1):
        y = round(b * sqrt(1.0 - x ** 2 / a / a))
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

    for y in range(0, b + 1, 1):
        x = round(a * sqrt(1.0 - y ** 2 / b / b))
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def ellips_param(win, cx, cy, a, b):
    m = max(a, b)
    k = round(pi * m / 2)
    for i in range(0, k + 1, 1):
        x = round(a * cos(i / m))
        y = round(b * sin(i / m))
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())


def ellips_brez(win, cx, cy, a, b):
    x = 0  # начальные значения
    y = b
    a = a ** 2
    d = round(b * b / 2 - a * b * 2 + a / 2)
    b = b ** 2
    while y >= 0:
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())

        if d < 0:  # пиксель лежит внутри эллипса
            buf = 2 * d + 2 * a * y - a
            x += 1
            if buf <= 0:  # горизотальный шаг
                d = d + 2 * b * x + b
            else:  # диагональный шаг
                y -= 1
                d = d + 2 * b * x - 2 * a * y + a + b
        elif d > 0:  # пиксель лежит вне эллипса
            buf = 2 * d - 2 * b * x - b
            y -= 1

            if buf > 0:  # вертикальный шаг
                d = d - 2 * y * a + a
            else:  # диагональный шаг
                x += 1
                d = d + 2 * x * b - 2 * y * a + a + b
        elif d == 0.0:  # пиксель лежит на окружности
            x += 1  # диагональный шаг
            y -= 1
            d = d + 2 * x * b - 2 * y * a + a + b


def ellips_middle(win, cx, cy, a, b):
    x = 0   # начальные положения
    y = b
    p = b ** 2 - a ** 2 * b + (a ** 2) / 4   # начальное значение параметра принятия решения в области tg<1
    while (b ** 2) * x < (a ** 2) * y:  # пока тангенс угла наклона меньше 1
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        x += 1

        if p < 0:  # средняя точка внутри эллипса, ближе верхний пиксел, горизонтальный шаг
            p += 2 * b ** 2 * x + b ** 2
        else:   # средняя точка вне эллипса, ближе диагональный пиксел, диагональный шаг
            y -= 1
            p += 2 * b ** 2 * x + b ** 2 - 2 * a ** 2 * y

    p = b ** 2 * (x + 0.5) ** 2 + a ** 2 * (y - 1) ** 2 - a ** 2 * b ** 2
    # начальное значение параметра принятия решения в области tg>1 в точке (х + 0.5, y - 1) последнего положения

    while y >= 0:
        win.image.setPixel(cx - x, cy + y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx - x, cy - y, win.pen.color().rgb())
        win.image.setPixel(cx + x, cy + y, win.pen.color().rgb())

        y -= 1

        if p > 0:
            p += -2 * a ** 2 * y + a ** 2
        else:
            x += 1
            p += -2 * a ** 2 * y + a ** 2 + 2 * b ** 2 * x


def draw_once(win):
    is_standart = False
    x = win.centr_x.value()
    y = win.centr_y.value()

    if win.circle.isChecked():
        r = win.rad.value()

        if win.canon.isChecked():
            circle_canon(win, x, y, r)
        elif win.param.isChecked():
            circle_param(win, x, y, r)
        elif win.brez.isChecked():
            circle_brez(win, x, y, r)
        elif win.middle.isChecked():
            circle_middle(win, x, y, r)
        elif win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - r, y - r, r * 2, r * 2, win.pen)
    elif win.ellips.isChecked():
        a = win.a.value()
        b = win.b.value()

        if win.canon.isChecked():
            ellips_canon(win, x, y, b, a)
        elif win.param.isChecked():
            ellips_param(win, x, y, b, a)
        elif win.brez.isChecked():
            ellips_brez(win, x, y, b, a)
        elif win.middle.isChecked():
            ellips_middle(win, x, y, b, a)
        elif win.lib.isChecked():
            is_standart = True
            win.scene.addEllipse(x - b, y - a, b * 2, a * 2, win.pen)

    if not is_standart:
        pix = QPixmap(611, 611)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


def draw_spectrum(win):
    is_standart = False
    x = win.centr_x.value()
    y = win.centr_y.value()
    d = win.dia.value()
    c = win.count.value()

    if win.circle.isChecked():
        for i in range(d, d * c + d, d):
            if win.canon.isChecked():
                circle_canon(win, x, y, i)
            elif win.param.isChecked():
                circle_param(win, x, y, i)
            elif win.brez.isChecked():
                circle_brez(win, x, y, i)
            elif win.middle.isChecked():
                circle_middle(win, x, y, i)
            elif win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - i, y - i, i * 2, i * 2, win.pen)
    elif win.ellips.isChecked():
        a = win.a.value()
        b = win.b.value()

        for i in range(d, d * c + d, d):
            if win.canon.isChecked():
                ellips_canon(win, x, y, b + i, a + i)
            elif win.param.isChecked():
                ellips_param(win, x, y, b + i, a + i)
            elif win.brez.isChecked():
                ellips_brez(win, x, y, b + i, a + i)
            elif win.middle.isChecked():
                ellips_middle(win, x, y, b + i, a + i)
            elif win.lib.isChecked():
                is_standart = True
                win.scene.addEllipse(x - (b + i), y - (a + i), (b + i) * 2, (a + i) * 2, win.pen)

    if not is_standart:
        pix = QPixmap(611, 611)
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)


def get_color_bground(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.white, title='Цвет фона',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_bground = color
        win.image.fill(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.bground_color.setScene(s)
        win.scene.setBackgroundBrush(color)


def get_color_line(win):
    color = QtWidgets.QColorDialog.getColor(initial=Qt.black, title='Цвет линии',
                                            options=QtWidgets.QColorDialog.DontUseNativeDialog)
    if color.isValid():
        win.color_line = color
        win.pen.setColor(color)
        s = QtWidgets.QGraphicsScene(0, 0, 10, 10)
        s.setBackgroundBrush(color)
        win.line_color.setScene(s)


def clear_all(win):
    win.image.fill(win.color_bground)
    win.scene.clear()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
