import numpy.linalg
from numpy import matrix, sign
import copy


def get_vect(dot_start, dot_end):
    return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]


def get_vect_mul(f_vector, s_vector):
    return f_vector[0] * s_vector[1] - f_vector[1] * s_vector[0]


def check_convexity_polygon(cutter):
    if len(cutter) < 3:
        return False

    vect1 = get_vect(cutter[0], cutter[1])
    vect2 = get_vect(cutter[1], cutter[2])

    s = -1
    if get_vect_mul(vect1, vect2) > 0:
        s = 1

    for i in range(len(cutter)):
        vect_i = get_vect(cutter[i - 2], cutter[i - 1])
        vect_j = get_vect(cutter[i - 1], cutter[i])

        if s * get_vect_mul(vect_i, vect_j) < 0:
            return False

    if s < 0:
        cutter.reverse()

    return True


def visibility(point, begin, end):
    tmp1 = (point[0] - begin[0]) * (end[1] - begin[1])
    tmp2 = (point[1] - begin[1]) * (end[0] - begin[0])
    res = tmp1 - tmp2

    if -1e-7 < res < 1e-7:
        res = 0
    return sign(res)


def check_lines_crossing(begin1, end1, begin2, end2):
    vis1 = visibility(begin1, begin2, end2)
    vis2 = visibility(end1, begin2, end2)

    if (vis1 < 0 < vis2) or (vis1 > 0 > vis2):
        return True
    else:
        return False


def get_cross_point(p_begin, p_end, q_begin, q_end):
    koef = [[p_end[0] - p_begin[0], -(q_end[0] - q_begin[0])],
            [p_end[1] - p_begin[1], -(q_end[1] - q_begin[1])]]

    rights = [q_begin[0] - p_begin[0],
              q_begin[1] - p_begin[1]]

    res = numpy.linalg.solve(koef, rights)

    # koef_tmp = matrix(koef)
    # koef_tmp = koef_tmp.I
    # koef = [[koef_tmp.item(0), koef_tmp.item(1)], [koef_tmp.item(2), koef_tmp.item(3)]]
    #
    # koef_tmp = matrix(koef)
    # param = koef_tmp.__mul__(rights)

    x, y = p_begin[0] + (p_end[0] - p_begin[0]) * res[0], p_begin[1] + (p_end[1] - p_begin[1]) * res[0]

    return [x, y]


def sutherland_hojman(polygon, clipper):
    p = polygon
    w = clipper

    np = len(p)
    nw = len(w)

    s = None
    f = None
    # цикл по всем ребрам отсекателя
    for i in range(nw - 1):
        # обнуление результата на текущем шаге
        nq = 0
        q = []
        # цикл по всем ребрам отсекаемого многоугольника
        for j in range(np):
            # если это первая вершина, запомнить
            if j == 0:
                f = p[j]
            else:
                # если не первая, проверить, есть ли пересечение с отсекателем
                if check_lines_crossing(s, p[j], w[i], w[i + 1]):
                    q.append(get_cross_point(s, p[j], w[i], w[i + 1]))  # добавить в результат точку пересечения
                    nq += 1
                else:
                    # если пересечения нет, проверить, не лежит ли на ребре
                    if visibility(s, w[i], w[i + 1]) == 0:
                        q.append(s)
                        nq += 1

            # обновить предыдущую вершину
            if visibility(p[j], w[i], w[i + 1]) <= 0:
                q.append(p[j])
                nq += 1
            s = p[j]

        # результат пуст => многоугольник невидим
        if nq == 0:
            return [], 0

        # последнее ребро отсекаемого многоугольника
        if check_lines_crossing(s, f, w[i], w[i + 1]):
            q.append(get_cross_point(s, f, w[i], w[i + 1]))
            nq += 1

        # обновление многоугольника
        p = q
        np = nq

    return p, np



