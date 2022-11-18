import curses
import random

from async_tools import sleep
from settings import STAR_FRAMES


def make_stars(canvas, canvas_height, canvas_width):
    number_of_stars = random.randint(25, 100)
    coroutines = []
    for _ in range(number_of_stars):
        row = random.randint(2, canvas_height - 2)
        column = random.randint(2, canvas_width - 2)
        star = random.choice(STAR_FRAMES)
        coroutine = blink(canvas, row, column, symbol=star)
        coroutines.append(coroutine)
    return coroutines


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        await sleep(random.randint(1, 20))

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 3))

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        await sleep(random.randint(1, 5))

        canvas.addstr(row, column, symbol)
        await sleep(random.randint(1, 3))
