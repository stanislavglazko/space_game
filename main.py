import asyncio
import curses
import random
import time

from itertools import cycle

from physics import update_speed
from space_garbage import fly_garbage
from tools import read_controls, draw_frame, fire, get_frame_size

PATH_TO_ANIMATION = './animations/'
FRAMES_FOR_GARBAGE = ['trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
SHIP_FRAMES = ['rocket_frame_1.txt', 'rocket_frame_2.txt']
STARS = '+*.:'


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


async def animate_spaceship(canvas, row, column, ships_height, ships_width, height, width, ship_frame_1, ship_frame_2):
    ships = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]
    row_speed = column_speed = 0
    iterator = cycle(ships)
    current_frame = next(iterator)
    for frame in iterator:
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, current_frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        if row + row_speed > 0 and row + row_speed + ships_height < height:
            row += row_speed
        if column + column_speed > 0 and column + column_speed + ships_width < width:
            column += column_speed
        draw_frame(canvas, row, column, frame)
        current_frame = frame
        time.sleep(0)
        await sleep()


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


def make_stars(canvas, height, width):
    number_of_stars = random.randint(25, 100)
    coroutines = []
    for _ in range(number_of_stars):
        row = random.randint(2, height - 2)
        column = random.randint(2, width - 2)
        star = random.choice(STARS)
        coroutine = blink(canvas, row, column, symbol=star)
        coroutines.append(coroutine)
    return coroutines


async def fill_orbit_with_garbage(coroutines, canvas, width):
    garbage_frames = make_garbage_frames()
    while True:
        coroutines.append(fly_garbage(canvas, random.randint(0, width), random.choice(garbage_frames)))
        await sleep()


def make_garbage_frames():
    frames = []
    for frame in FRAMES_FOR_GARBAGE:
        with open(f'{PATH_TO_ANIMATION}{frame}') as garbage_file:
            frame = garbage_file.read()
            frames.append(frame)
    return frames


def make_shot(canvas, height, width):
    start_row, start_column = height // 2, width // 2
    shot = fire(canvas, start_row, start_column)
    return shot


def make_ship(canvas, height, width):
    with open(f'{PATH_TO_ANIMATION}{SHIP_FRAMES[0]}', 'r') as frame1:
        ship_frame1 = frame1.read()
    with open(f'{PATH_TO_ANIMATION}{SHIP_FRAMES[1]}', 'r') as frame2:
        ship_frame2 = frame2.read()
    ships_height, ships_width = get_frame_size(ship_frame1)
    start_row = (height // 2) - (ships_height // 2)
    start_column = (width // 2) - (ships_width // 2)
    spaceship = animate_spaceship(canvas,
                                  start_row,
                                  start_column,
                                  ships_height,
                                  ships_width,
                                  height,
                                  width,
                                  ship_frame1,
                                  ship_frame2,
                                  )
    return spaceship


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = []
    height, width = canvas.getmaxyx()
    coroutines.extend(make_stars(canvas, height, width))
    coroutines.append(fill_orbit_with_garbage(coroutines, canvas, width))
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
