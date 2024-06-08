from math import sqrt

def get_bit_cod_point(rectangle, point):
    bit = 0b0000
    #   x < x_лев
    if point[0] < rectangle[0]:
        bit += 0b0001
    # x > x_прав
    if point[0] > rectangle[1]:
        bit += 0b0010
    # y < y_низ
    if point[1] < rectangle[2]:
        bit += 0b0100
    # y > y_верх
    if point[1] > rectangle[3]:
        bit += 0b1000
    return bit


def t_arr(rect, point):
    x = point[0]
    y = point[1]
    xl = rect[0]
    xr = rect[1]
    yd = rect[2]
    yu = rect[3]

    t = [0, 0, 0, 0]
    t[0] = 1 if x < xl else 0
    t[1] = 1 if x > xr else 0
    t[2] = 1 if y < yd else 0
    t[3] = 1 if y > yu else 0

    return t


def count_s(t):
    return sum(t)


def multy(t1, t2):
    mul = 0
    for i in range(4):
        mul += t1[i] * t2[i]
    return mul


def mid_point_algorithm(rectangle, line):
    # инициализация
    eps, i = sqrt(2), 1
    p1 = [line[0][0], line[0][1]]
    p2 = [line[1][0], line[1][1]]

    res = None
    while res is None:
        # вычисление кодов точек p1 и p2
        t1 = t_arr(rectangle, p1)
        t2 = t_arr(rectangle, p2)

        # вычисление сумм кодов концов
        s1, s2 = count_s(t1), count_s(t2)

        # отрезок полностью видим?
        if s1 == 0 and s2 == 0:
            res = [p1, p2]
            break

        # отрезок тривиально невидим?
        if multy(t1, t2) != 0:
            res = []
            break

        # поиск наиболее удаленной от p1 видимой точки

        r = p1
        if i > 2:
            if multy(t1, t2) != 0:
                res = []
                break
            else:
                res = [p1, p2]
                break

        # точка p2 видима?
        if s2 == 0:
            # поиск наиболее удаленной от p2 видимой точки (перемена мест p1, p2)
            p1 = p2
            p2 = r
            i += 1
            continue

        # пересечение не обнаружено?
        while get_len(p1, p2) >= eps:
            # вычисление средней точки
            pm = [(p1[0] + p2[0]) / 2, (p1[1] + p2[1]) / 2]
            p = p1
            p1 = pm
            # новый код для p1
            t1 = t_arr(rectangle, p1)

            if multy(t1, t2) != 0:  # не видим
                # продолжить работу с p1pm
                p1 = p
                p2 = pm
            # иначе с pmp2
        else:
            p1 = p2
            p2 = r
            i += 1
            continue

    return res


def get_len(p1, p2):
    return sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def find_visibility(t1, t2):
    s1 = count_s(t1)
    s2 = count_s(t2)

    if s1 == 0 and s2 == 0:
        pr = 1
    else:
        pl = multy(t1, t2)
        if pl == 1:
            pr = -1
        else:
            pr = 0
    return pr
