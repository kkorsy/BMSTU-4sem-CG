import time


def sign(x):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0


def draw_brezenhem_float(canvas, xn, yn, xk, yk, color, draw=True, stepmode=False):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    delta_x, delta_y = xk - xn, yk - yn
    sx, sy = sign(delta_x), sign(delta_y)
    delta_x, delta_y = abs(delta_x), abs(delta_y)

    if delta_y > delta_x:
        delta_x, delta_y = delta_y, delta_x
        exchange = 1
    else:
        exchange = 0

    m = delta_y / delta_x
    e = m - 0.5
    x, y = xn, yn

    xb = x
    yb = y
    steps = 0

    for i in range(delta_x):
        if draw:
            canvas.create_line(x, y, x + 1, y, fill=color)
        if e >= 0:
            if exchange:
                x = x + sx
            else:
                y = y + sy
            e -= 1

        if exchange:
            y = y + sy
        else:
            x = x + sx
        e += m

        if stepmode:
            if xb != x and yb != y:
                steps += 1
            xb = x
            yb = y

    if stepmode:
        return steps


def draw_brezenhem_int(canvas, xn, yn, xk, yk, color, draw=True, stepmode=False):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    delta_x, delta_y = xk - xn, yk - yn
    sx, sy = sign(delta_x), sign(delta_y)
    delta_x, delta_y = abs(delta_x), abs(delta_y)

    if delta_y > delta_x:
        delta_x, delta_y = delta_y, delta_x
        exchange = 1
    else:
        exchange = 0

    e = 2 * delta_y - delta_x
    x, y = xn, yn

    xb = x
    yb = y
    steps = 0

    for i in range(delta_x):
        if draw:
            canvas.create_line(x, y, x + 1, y, fill=color)
        if e >= 0:
            if exchange:
                x = x + sx
            else:
                y = y + sy
            e -= 2 * delta_x

        if exchange:
            y = y + sy
        else:
            x = x + sx
        e += 2 * delta_y

        if stepmode:
            if xb != x and yb != y:
                steps += 1
            xb = x
            yb = y

    if stepmode:
        return steps


# Массив цветов одного оттенка разной интенсивности
def get_rgb_intensity(canvas, color, bg_color, intensity):
    gradient = []
    (r1, g1, b1) = canvas.winfo_rgb(color)  # разложение цвета линни на составляющие ргб
    (r2, g2, b2) = canvas.winfo_rgb(bg_color)   # разложение цвета фона на составляющие ргб
    r_step = float(r2 - r1) / intensity    # получение шага интенсивности
    g_step = float(g2 - g1) / intensity
    b_step = float(b2 - b1) / intensity

    for i in range(intensity):
        nr = int(r1 + (r_step * i))    # заполнение массива разными оттенками
        ng = int(g1 + (g_step * i))
        nb = int(b1 + (b_step * i))
        gradient.append("#%4.4x%4.4x%4.4x" % (nr, ng, nb))
    gradient.reverse()

    return gradient


def draw_brezenhem_gradation(canvas, xn, yn, xk, yk, color, bg_color, draw=True, stepmode=False):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    delta_x, delta_y = xk - xn, yk - yn
    sx, sy = sign(delta_x), sign(delta_y)
    delta_x, delta_y = abs(delta_x), abs(delta_y)

    if delta_y > delta_x:
        delta_x, delta_y = delta_y, delta_x
        exchange = 1
    else:
        exchange = 0

    I = 100  # кол-во уровней интенсивности
    m = delta_y / delta_x * I
    t1 = time.time()
    gradient = get_rgb_intensity(canvas, color, bg_color, I)
    t2 = time.time()

    e = I / 2   # интенсивность первого пикселя
    x, y = xn, yn
    w = I - m

    xb = x
    yb = y
    steps = 0

    for i in range(delta_x):
        if draw:
            canvas.create_line(x, y, x + 1, y, fill=gradient[round(e) - 1])
        if e < w:
            if exchange:
                y += sy
            else:
                x += sx
            e += m
        else:
            x += sx
            y += sy
            e -= w

        if stepmode:
            if xb != x and yb != y:
                steps += 1
            xb = x
            yb = y

    if stepmode:
        return steps
    return t2 - t1
