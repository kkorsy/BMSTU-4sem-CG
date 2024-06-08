def draw_lines(canvas, lines):
    for line in lines:
        if len(line) == 3:
            canvas.create_line(line[0], line[1], fill=line[2])


def set_pixel(canvas, x, y, color):
    canvas.create_line(x, y, x + 1, y, fill=color)


def add_vertex_clipper(canvas, clipper, point, color):
    if not clipper:
        set_pixel(canvas, point[0], point[1], color)
    else:
        canvas.create_line(clipper[-1], point, fill=color)

    clipper.append(point)


def close_clipper(canvas, clipper, color):
    canvas.create_line(clipper[-1], clipper[0], fill=color)


def add_line(canvas, lines, xb, yb, xe, ye, linecolor):
    canvas.create_line([xb, yb], [xe, ye], fill=linecolor)

    lines.append([])
    lines[-1].append([xb, yb])
    lines[-1].append([xe, ye])
    lines[-1].append(linecolor)
