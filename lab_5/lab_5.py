from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QTableWidgetItem
from PyQt5.QtGui import QPen, QColor, QImage, QPixmap, QPainter
from PyQt5.QtCore import Qt, QEventLoop, QPoint
import time, math

black, red, green, yellow, blue, white = Qt.black, Qt.red, Qt.green, Qt.yellow, Qt.blue, Qt.white


class Window(QtWidgets.QMainWindow):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        uic.loadUi("window.ui", self)
        self.scene = MyScene(0, 0, 561, 581)
        self.scene.win = self
        self.view.setScene(self.scene)
        self.image = QImage(561, 581, QImage.Format_ARGB32_Premultiplied)
        self.image.fill(Qt.white)
        self.lock.clicked.connect(lambda: lock(self))
        self.erase.clicked.connect(lambda: clean_all(self))
        self.paint.clicked.connect(lambda: fill_sorted_list(self))
        self.addpoint.clicked.connect(lambda: add_point_by_btn(self))

        self.black_fill_btn.clicked.connect(lambda: change_color(self, black))
        self.red_fill_btn.clicked.connect(lambda: change_color(self, red))
        self.green_fill_btn.clicked.connect(lambda: change_color(self, green))
        self.yellow_fill_btn.clicked.connect(lambda: change_color(self, yellow))
        self.blue_fill_btn.clicked.connect(lambda: change_color(self, blue))
        self.white_fill_btn.clicked.connect(lambda: change_color(self, white))

        self.edges = []
        self.point_now = None
        self.point_lock = None
        self.pen = QPen(black)
        self.delay.setChecked(False)


class MyScene(QtWidgets.QGraphicsScene):
    def mousePressEvent(self, event):
        add_point(event.scenePos())


class Edge:
    def __init__(self, x, n, dy, dx):
        self.x = x
        self.n = n
        self.dy = dy
        self.dx = dx


def change_color(win, color):
    win.black_fill_btn.setChecked(False)
    win.red_fill_btn.setChecked(False)
    win.green_fill_btn.setChecked(False)
    win.yellow_fill_btn.setChecked(False)
    win.blue_fill_btn.setChecked(False)
    win.white_fill_btn.setChecked(False)
    if color == black:
        win.black_fill_btn.setChecked(True)
    elif color == red:
        win.red_fill_btn.setChecked(True)
    elif color == green:
        win.green_fill_btn.setChecked(True)
    elif color == yellow:
        win.yellow_fill_btn.setChecked(True)
    elif color == blue:
        win.blue_fill_btn.setChecked(True)
    else:
        win.white_fill_btn.setChecked(True)
    # win.pen.setColor(color)


def color_pixels(win, cap, cur_y, color):
    x_list = list(int(i.x) for i in cap)
    x_list.sort()
    diff = 0

    pix = QPixmap()
    p = QPainter()
    p.begin(win.image)
    p.setPen(QPen(color))
    for i in range(0, len(x_list), 2):
        for x in range(x_list[i], x_list[i + 1]):
            p.drawPoint(x, int(cur_y))
        t1 = time.time()
        if win.delay.isChecked():
            delay()
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)
        else:
            pix.convertFromImage(win.image)
            win.scene.addPixmap(pix)
        t2 = time.time()
        diff += t2 - t1
    p.end()

    return diff


def identify_color(win):
    # win.pen = QPen(black)
    if win.black_fill_btn.isChecked():
        return black
    if win.red_fill_btn.isChecked():
        # win.pen = QPen(red)
        return red
    if win.green_fill_btn.isChecked():
        # win.pen = QPen(green)
        return green
    if win.yellow_fill_btn.isChecked():
        # win.pen = QPen(yellow)
        return yellow
    if win.blue_fill_btn.isChecked():
        # win.pen = QPen(blue)
        return blue
    # win.pen = QPen(white)
    return white


def is_local(x, edges):
    r1, r2 = list(), list()
    for i in edges:
        if i[0] == x:
            r1 = i
        if i[2] == x:
            r2 = i
    if len(r1) != 0 and len(r2) != 0 and ((r1[1] > r1[3] and r2[3] > r2[1]) or (r1[1] < r1[3] and r2[3] < r2[1])):
        return True
    return False


def fill_sorted_list(win):
    pix = QPixmap()
    p = QPainter()
    p.begin(win.image)

    p.setPen(QPen(black))
    for ed in win.edges:
        p.drawLine(int(ed[0]), int(ed[1]), int(ed[2]), int(ed[3]))

    color = identify_color(win)
    t1 = time.time()

    # подготовка
    edges = list()
    for e in win.edges:
        if e[1] == e[3]:
            continue

        n = max(e[1], e[3])
        if n == e[1]:
            x = e[0]
        else:
            x = e[2]
        dy = abs(e[3] - e[1])
        if x == e[0]:
            dx = (e[2] - e[0]) / dy
        else:
            dx = (e[0] - e[2]) / dy
        edges.append(Edge(x, n, dy, dx))

    # сортировка
    for i in range(len(edges)):
        for j in range(i + 1, len(edges)):
            if edges[j].n > edges[i].n:
                edges[i], edges[j] = edges[j], edges[i]

    # алгоритм
    cap = list()
    y = edges[0].n
    pos = 0
    count_edges = len(edges)
    diff_time = 0
    
    while y > 0:
        if pos != 0 and len(cap) == 0:
            break

        for j in range(count_edges):
            if edges[j].n == y and edges[j].x > 0:
                cap.append(edges[j])
                pos = j + 1

        x_list = list(int(i.x) for i in cap)
        # flag = False
        # if len(x_list) % 2 != 0:
        #     flag = True
        # for i in range(len(x_list)):
        #     if flag and is_local(x_list[i], win.edges):
        #         x_list.append(x_list[i])
        #         i += 1
        x_list.sort()

        dt = 0
        p.setPen(QPen(color))
        for i in range(0, len(x_list), 2):
            for x in range(x_list[i], x_list[i + 1]):
                p.drawPoint(x, int(y))
            t3 = time.time()
            if win.delay.isChecked():
                delay()
                pix.convertFromImage(win.image)
                win.scene.addPixmap(pix)
            t4 = time.time()
            dt += t4 - t3

        y -= 1
        for i in cap:
            i.dy -= 1
            i.x += i.dx

        i = 0
        while i < len(cap):
            if cap[i].dy <= 0:
                del cap[i]
            else:
                i += 1
        diff_time += dt

    t2 = time.time()
    t = (t2 - t1 - diff_time) * 100
    win.time.display(t)
    if not win.delay.isChecked():
        pix.convertFromImage(win.image)
        win.scene.addPixmap(pix)

    p.setPen(QPen(black))
    for ed in win.edges:
        p.drawLine(int(ed[0]), int(ed[1]), int(ed[2]), int(ed[3]))

    p.end()


def add_row(win):
    win.table.insertRow(win.table.rowCount())


def add_point(point):
    global w
    if w.point_now is None:
        w.point_now = point
        w.point_lock = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
    else:
        w.edges.append([w.point_now.x(), w.point_now.y(),
                        point.x(), point.y()])
        w.point_now = point
        add_row(w)
        i = w.table.rowCount() - 1
        item_x = QTableWidgetItem("{0}".format(point.x()))
        item_y = QTableWidgetItem("{0}".format(point.y()))
        w.table.setItem(i, 0, item_x)
        w.table.setItem(i, 1, item_y)
        item_x = w.table.item(i - 1, 0)
        item_y = w.table.item(i - 1, 1)
        w.pen.setColor(black)
        w.scene.addLine(point.x(), point.y(), float(item_x.text()), float(item_y.text()), w.pen)


def lock(win):
    win.edges.append([win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y()])
    win.scene.addLine(win.point_now.x(), win.point_now.y(), win.point_lock.x(), win.point_lock.y(), w.pen)
    win.point_now = None


def clean_all(win):
    win.scene.clear()
    win.table.clear()
    win.edges = []
    win.point_now = None
    win.point_lock = None
    win.image.fill(white)
    r = win.table.rowCount()
    for i in range(r, -1, -1):
        win.table.removeRow(i)


def draw_edges(image, edges):
    p = QPainter()
    p.begin(image)
    p.setPen(QPen(black))
    for ed in edges:
        p.drawLine(int(ed[0]), int(ed[1]), int(ed[2]), int(ed[3]))
    p.end()
    # global w
    #
    # qp = QPainter()
    # qp.begin(w)
    #
    # pen = QPen(Qt.black, 2, Qt.SolidLine)
    # qp.setPen(pen)
    # for i in w.edges:
    #     qp.drawLine(int(i[0]), int(i[1]), int(i[2]), int(i[3]))
    #
    # qp.end()

    # global w
    # w.pen.setColor(black)
    # for ed in w.edges:
    #     w.scene.addLine(ed[0], ed[1], ed[2], ed[3], w.pen)


def delay():
    QtWidgets.QApplication.processEvents(QEventLoop.AllEvents, 1)


def add_point_by_btn(win):
    x = win.x.value()
    y = win.y.value()
    p = QPoint()
    p.setX(x)
    p.setY(y)
    add_point(p)


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    w = Window()
    w.show()
    sys.exit(app.exec_())
