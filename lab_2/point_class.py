class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        if self.x < other.x:
            return True
        return False


class History:
    def __init__(self):
        self.cur = -1
        self.list = list()

    def is_last(self):
        if self.cur == -1:
            return True
        return False

    def is_first(self):
        if self.cur == len(self.list) - 1:
            return True
        return False

    def get_prev(self):
        self.cur -= 1
        return self.list[self.cur + 1]

    def get_next(self):
        self.cur += 1
        return self.list[self.cur]

    def append_new(self, matrix):
        if not self.is_first():
            self.list = self.list[:self.cur + 1]
        self.list.append(matrix)
        self.cur += 1


class Crossing:
    def __init__(self, x1, y1, x2, y2, x3, y3):
        self.one = Point(x1, y1)
        self.two = Point(x2, y2)
        self.three = Point(x3, y3)
