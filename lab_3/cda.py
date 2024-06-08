def draw_cda(canvas, xn, yn, xk, yk, color, draw=True, stepmode=False):
    if draw and xn == xk and yn == yk:
        canvas.create_line(round(xn), round(yn), round(xk + 1), round(yk), fill=color)
        return

    steps = 0
    delta_x, delta_y = xk - xn, yk - yn
    if abs(delta_x) > abs(delta_y):
        l = abs(delta_x)
    else:
        l = abs(delta_y)
    delta_x, delta_y = delta_x / l, delta_y / l
    x, y = xn, yn
    for i in range(l):
        round(x)
        if draw:
            canvas.create_line(round(x), round(y), round(x + 1), round(y), fill=color)
        if stepmode and round(x + delta_x) != round(x) and round(y + delta_y) != round(y):
            steps += 1
        x = x + delta_x
        y = y + delta_y

    if stepmode:
        return steps
