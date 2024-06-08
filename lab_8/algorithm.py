def scalar_mul(f_vector, s_vector):
    return f_vector[0] * s_vector[0] + f_vector[1] * s_vector[1]


def get_vector(dot_start, dot_end):
    return [dot_end[0] - dot_start[0], dot_end[1] - dot_start[1]]


def get_vector_mul(f_vector, s_vector):
    return f_vector[0] * s_vector[1] - f_vector[1] * s_vector[0]


def check_convexity_polygon(cutter):
    if len(cutter) < 3:
        return False

    vector1 = get_vector(cutter[0], cutter[1])
    vector2 = get_vector(cutter[1], cutter[2])

    if get_vector_mul(vector1, vector2) > 0:
        sign = 1
    else:
        sign = -1

    for i in range(len(cutter)):
        vector_i = get_vector(cutter[i - 2], cutter[i - 1])
        vector_j = get_vector(cutter[i - 1], cutter[i])

        if sign * get_vector_mul(vector_i, vector_j) < 0:
            return False

    if sign < 0:
        cutter.reverse()

    return True


def get_normal(dot1, dot2, dot3):
    vector = get_vector(dot1, dot2)

    if vector[1]:
        normal = [1, - vector[0] / vector[1]]
    else:
        normal = [0, 1]

    if scalar_mul(get_vector(dot2, dot3), normal) < 0:
        normal[0] = - normal[0]
        normal[1] = - normal[1]

    return normal


def cyrus_beck_alg(canvas, clipper_figure, line, res_color):
    # инициализация пределов значений параметра t при условии, что отрезок полностью видим
    t_beg = 0
    t_end = 1

    # точки р1 и р2
    dot1 = line[0]
    dot2 = line[1]

    # директриса
    d = [dot2[0] - dot1[0], dot2[1] - dot1[1]]

    # цикл по всем сторонам отсекателя
    for i in range(-2, len(clipper_figure) - 2):
        # вычисление внутренней нормали к текущей стороне отсекателя
        normal = get_normal(clipper_figure[i], clipper_figure[i + 1], clipper_figure[i + 2])

        # вектор Wi = P1 - f, где f - граничная точка стороны отсекателя
        w = [dot1[0] - clipper_figure[i][0],
             dot1[1] - clipper_figure[i][1]]

        # позволяет определить ближе к началу или концу расположена точка перечения =>
        # => определяет она начало или конец видимой части
        d_scalar = scalar_mul(d, normal)

        # положение первой вершины отрезка относительно границы отсекателя
        # w_scalar >= 0 - отрезок видимый для текущей стороны отсекателя
        # w_scalar < 0 - отрезок полностью невидимый
        w_scalar = scalar_mul(w, normal)

        # вырождение отрезка в точку или его параллельность стороне отсекателя
        if d_scalar == 0:
            if w_scalar < 0:
                return  # отрезок (точка) невидима
            else:
                continue    # отрезок (точка) видима относительно текущей стороны

        # параметр t
        t = - w_scalar / d_scalar

        # поиск нижней границы параметра t
        if d_scalar > 0:
            if t <= 1:
                t_beg = max(t_beg, t)   # нижняя граница => максимальное значение
            else:
                return  # нижний предел параметра t > 1 => продолжение отрезка за Р2 пересекает отсекатель
        # поиск верхней границы параметра t
        elif d_scalar < 0:
            if t >= 0:
                t_end = min(t_end, t)   # верхняя граница => минимальное значение
            else:
                return  # верхний предел параметра t < 0 => продолжение отрезка за Р1 пересекает отсекатель

        # дополнительная проверка на видимость
        if t_beg > t_end:
            break

    # отрисовка в случае успешного выхода из цикла
    if t_beg <= t_end:
        dot1_res = [round(dot1[0] + d[0] * t_beg), round(dot1[1] + d[1] * t_beg)]
        dot2_res = [round(dot1[0] + d[0] * t_end), round(dot1[1] + d[1] * t_end)]

        canvas.create_line(dot1_res, dot2_res, fill=res_color)
