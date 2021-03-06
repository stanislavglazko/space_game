import asyncio
import curses
import random
import time

from itertools import cycle

from tools import read_controls, draw_frame, fire, get_frame_size


async def animate_spaceship(canvas, row, column, ships_height, ships_width, height, width, ship_frame_1, ship_frame_2):
    ships = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]
    iterator = cycle(ships)
    current_frame = next(iterator)
    for frame in iterator:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, current_frame, negative=True)
        if (row + rows_direction) > 0:
            if (row + rows_direction + ships_height) < height:
                row += rows_direction
        if (column + columns_direction) > 0:
            if (column + columns_direction + ships_width) < width:
                column += columns_direction
        draw_frame(canvas, row, column, frame)
        current_frame = frame
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


def make_stars(canvas, height, width):
    number_of_stars = random.randint(25, 100)
    stars = '+*.:'
    coroutines = []
    for i in range(number_of_stars):
        row = random.randint(2, height - 2)
        column = random.randint(2, width - 2)
        star = random.choice(stars)
        coroutine = blink(canvas, row, column, symbol=star)
        coroutines.append(coroutine)
    return coroutines


def make_shot(canvas, height, width):
    start_row, start_column = height // 2, width // 2
    shot = fire(canvas, start_row, start_column)
    return shot


def make_ship(canvas, height, width):
    with open("./animations/rocket_frame_1.txt", "r") as frame1:
        ship_frame_1 = frame1.read()
    with open("./animations/rocket_frame_2.txt", "r") as frame2:
        ship_frame_2 = frame2.read()
    ships_height, ships_width = get_frame_size(ship_frame_1)
    start_row = (height // 2) - (ships_height // 2)
    start_column = (width // 2) - (ships_width // 2)
    spaceship = animate_spaceship(canvas,
                                  start_row,
                                  start_column,
                                  ships_height,
                                  ships_width,
                                  height,
                                  width,
                                  ship_frame_1,
                                  ship_frame_2,
                                  )
    return spaceship


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = []
    height, width = canvas.getmaxyx()
    coroutines.extend(make_stars(canvas, height, width))
    coroutines.append(make_shot(canvas, height, width))
    coroutines.append(make_ship(canvas, height, width))
    while True:
        for coroutine in coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
