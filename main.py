import tkinter as tk

WIDTH = 400
HEIGHT = 400

target = None; object = None
tx = WIDTH / 2; ty = HEIGHT / 2
ox = 0; oy = HEIGHT
tvx = 0; tvy = 0
ovx = 0; ovy = 0

canvas = None


def __init__():
    global target, object
    window = tk.Tk()
    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    cx = WIDTH / 2; cy = HEIGHT / 2
    target = canvas.create_oval(
        cx, cy, cx + WIDTH / 30, cy + HEIGHT / 30, fill="blue")
    object = canvas.create_oval(
        cx, HEIGHT - HEIGHT / 30, cx + WIDTH / 30, HEIGHT, fill="red")
    canvas.pack()
    loop(canvas)


def loop(canvas: tk.Canvas):
    while True:
        animate(canvas)
        canvas.update()


def animate(canvas: tk.Canvas):
    canvas.move(target, tvx, tvy)
    canvas.move(object, ovx, ovy)


if __name__ == "__main__":
    __init__()
