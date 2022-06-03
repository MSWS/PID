import tkinter as tk
from math import cos, sin
from time import sleep, time

WIDTH = 800
HEIGHT = 800

BALL_WIDTH = WIDTH / 30
BALL_HEIGHT = HEIGHT / 30

target, object = None, None
tvx, tvy = 0, 0
ovx, ovy = 0, 0
opidx, opidy = None, None
canvas = None
accel = 1
power = 20


def __init__():
    global target, object, opidx, opidy
    window = tk.Tk()
    canvas = tk.Canvas(window, width=WIDTH, height=HEIGHT)
    window.bind('<Motion>', lambda event: moveTarget(canvas, event))
    cx = WIDTH / 2; cy = HEIGHT / 2
    target = canvas.create_oval(
        cx, cy, cx + BALL_WIDTH, cy + BALL_HEIGHT, fill="blue")
    object = canvas.create_oval(
        cx, HEIGHT - BALL_HEIGHT, cx + BALL_HEIGHT, HEIGHT, fill="red")
    canvas.pack()
    opidx, opidy = PID(), PID()
    opidx.propWeight = 0.15
    opidx.derivWeight = 0.1
    opidx.intWeight = 0.01
    opidy.propWeight = 0.15
    opidy.derivWeight = 0.1
    opidy.intWeight = 0.01
    loop(canvas)


def loop(canvas: tk.Canvas):
    while True:
        move(canvas)
        canvas.update()
        sleep(0.01)


def move(canvas: tk.Canvas):
    global opidx, opidy, tvx, tvy, ovx, ovy
    print(canvas.coords(object))
    otvx = opidx.calculate(canvas.coords(object)[0], canvas.coords(target)[0])
    otvy = opidy.calculate(canvas.coords(object)[1], canvas.coords(target)[1])
    print("otvx", otvx, "otvy", otvy)

    otvx = clamp(otvx - ovx, -accel, accel)
    otvy = clamp(otvy - ovy, -accel, accel)

    ovx += otvx
    ovy += otvy

    ovx = clamp(ovx, -power, power)
    ovy = clamp(ovy, -power, power)

    # ovy += 0.1

    canvas.move(object, ovx, ovy)

    t = time() * 1000.0 / 400
    rad = WIDTH / 4
    # canvas.moveto(target, sin(t) * rad + WIDTH / 2)


def moveTarget(canvas, mouse):
    canvas.moveto(target, mouse.x - BALL_WIDTH / 2, mouse.y - BALL_HEIGHT / 2)


def clamp(value, minValue, maxValue):
    return max(min(value, maxValue), minValue)


class PID():
    def __init__(self):
        self.propWeight = 1.0
        self.intWeight = 0.01
        self.derivWeight = 0.2
        self.intGain = 0.005
        self.intSum = 0.0
        self.lastCheck = 0
        self.lastError = 0

    def calculate(self, current, target):
        error = target - current
        propVal = self.propWeight * error
        dt = time() * 1000 - self.lastCheck
        derVal = self.derivWeight * (error - self.lastError) / dt
        self.intSum += self.intGain * (error - self.lastError) / dt
        intVal = self.intSum * self.intWeight
        self.lastError = error
        self.lastCheck = time() * 1000
        print("propVal", propVal, "derVal", derVal, "intVal", intVal)
        return propVal + derVal + intVal


if __name__ == "__main__":
    __init__()
