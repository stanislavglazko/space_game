import asyncio
import curses
import random
import time

from itertools import cycle

from tools import read_controls, draw_frame, fire, get_frame_size


async def animate_spaceship(canvas, row, column, rows, columns, height, width, ship1, ship2):
    ships = [ship1, ship2]
    iterator = cycle(ships)
    frame = next(iterator)
    while True:
        for _ in range(2):
            draw_frame(canvas, row, column, frame, negative=True)
            rows_direction, columns_direction, space_pressed = read_controls(canvas)
            frame = next(iterator)
            if (row + rows_direction) > 0:
                if (row + rows_direction + rows) < height:
                    row += rows_direction
            if (column + columns_direction) > 0:
                if (column + columns_direction + columns) < width:
                    column += columns_direction
            draw_frame(canvas, row, column, frame)
            canvas.refresh()
            time.sleep(1)
        await asyncio.sleep(0)


async def blink(canvas, row, column, symbol='*'):
    while True:
        canvas.addstr(row, column, symbol, curses.A_DIM)
        for i in range(random.randint(1, 20)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(random.randint(1, 3)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol, curses.A_BOLD)
        for i in range(random.randint(1, 5)):
            await asyncio.sleep(0)

        canvas.addstr(row, column, symbol)
        for i in range(random.randint(1, 3)):
            await asyncio.sleep(0)


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = []
    number_of_stars = random.randint(25, 100)
    stars = '+*.:'
    height, width = canvas.getmaxyx()
    for i in range(number_of_stars):
        row = random.randint(2, height - 2)
        column = random.randint(2, width - 2)
        star = random.choice(stars)
        coroutine = blink(canvas, row, column, symbol=star)
        coroutines.append(coroutine)
    start_row, start_column = height // 2, width // 2
    shot = fire(canvas, start_row, start_column)
    coroutines.append(shot)
    with open("./animations/rocket_frame_1.txt", "r") as my_file:
        ship1 = my_file.read()
    with open("./animations/rocket_frame_2.txt", "r") as my_file:
        ship2 = my_file.read()
    rows, columns = get_frame_size(ship1)
    start_row = (height // 2) - (rows // 2)
    start_column = (width // 2) - (columns // 2)
    spaceship = animate_spaceship(canvas, start_row, start_column, rows, columns, height, width, ship1, ship2)
    coroutines.append(spaceship)
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
                canvas.refresh()
            except StopIteration:
                coroutines.remove(coroutine)
        time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
