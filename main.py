import asyncio
import curses
import random
import time

from itertools import cycle
from explosion import explode

from fire import fire
from physics import update_speed
from obstacles import obstacles, obstacles_in_last_collisions, show_obstacles
from space_garbage import fly_garbage
from tools import read_controls, draw_frame, get_frame_size

PATH_TO_ANIMATIONS = './animations/'
GARBAGE_FRAMES = ['trash_large.txt', 'trash_small.txt', 'trash_xl.txt']
SHIP_FRAMES = ['rocket_frame_1.txt', 'rocket_frame_2.txt']
STAR_FRAMES = '+*.:'
GAME_OVER_FRAME = 'game_over.txt'


async def sleep(tics=1):
    for _ in range(tics):
        await asyncio.sleep(0)


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


async def fill_orbit_with_garbage(coroutines, canvas, canvas_width):
    garbage_frames = get_garbage_frames()
    while True:
        coroutines.append(fly_garbage(obstacles, canvas, random.randint(0, canvas_width), random.choice(garbage_frames)))
        await sleep()
        return


def get_garbage_frames():
    frames = []
    for frame in GARBAGE_FRAMES:
        with open(f'{PATH_TO_ANIMATIONS}{frame}') as garbage_file:
            frame = garbage_file.read()
            frames.append(frame)
    return frames


def make_spaceship(coroutines, canvas, canvas_height, canvas_width):
    ship_frame1, ship_frame2 = get_ship_frames()
    ships_height, ships_width = get_frame_size(ship_frame1)
    start_row = (canvas_height // 2) - (ships_height // 2)
    start_column = (canvas_width // 2) - (ships_width // 2)
    animated_spaceship = animate_spaceship(
        coroutines,
        canvas,
        start_row,
        start_column,
        ships_height,
        ships_width,
        canvas_height,
        canvas_width,
        ship_frame1,
        ship_frame2,
    )
    return animated_spaceship


def get_ship_frames():
    with open(f'{PATH_TO_ANIMATIONS}{SHIP_FRAMES[0]}', 'r') as frame1:
        ship_frame1 = frame1.read()
    with open(f'{PATH_TO_ANIMATIONS}{SHIP_FRAMES[1]}', 'r') as frame2:
        ship_frame2 = frame2.read()
    return ship_frame1, ship_frame2


async def animate_spaceship(
    coroutines,
    canvas,
    start_row,
    start_column,
    ships_height,
    ships_width,
    canvas_height,
    canvas_width,
    ship_frame_1,
    ship_frame_2,
    ):
    row, column = start_row, start_column
    ship_frames = [ship_frame_1, ship_frame_1, ship_frame_2, ship_frame_2]
    row_speed = column_speed = 0
    iterator = cycle(ship_frames)
    current_ship_frame = next(iterator)
    for frame in iterator:
        for obstacle in obstacles:
            if obstacle.has_collision(row, column):
                draw_frame(canvas, row, column, current_ship_frame, negative=True)
                coroutines.append(show_game_over(canvas, start_row, start_column))
                return
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, current_ship_frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        if row + row_speed > 0 and row + row_speed + ships_height < canvas_height:
            row += row_speed
        if column + column_speed > 0 and column + column_speed + ships_width < canvas_width:
            column += column_speed
        if space_pressed:
            coroutines.append(fire(canvas, row, column + ships_width // 2, rows_speed=-1))
        draw_frame(canvas, row, column, frame)
        current_ship_frame = frame
        time.sleep(0)
        await sleep()


async def show_game_over(canvas, start_row, start_column):
    game_over_frame = get_game_over_frame()
    _, frame_width = get_frame_size(game_over_frame)
    updated_start_column = start_column - frame_width // 2
    while True:
        draw_frame(canvas, start_row, updated_start_column, game_over_frame)
        await sleep()


def get_game_over_frame():
    with open(f'{PATH_TO_ANIMATIONS}{GAME_OVER_FRAME}', 'r', encoding="utf-8") as frame:
        game_over_frame = frame.read()
    return game_over_frame


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = []
    canvas_height, canvas_width = canvas.getmaxyx()
    coroutines.extend(make_stars(canvas, canvas_height, canvas_width))
    coroutines.append(fill_orbit_with_garbage(coroutines, canvas, canvas_width))
    coroutines.append(show_obstacles(canvas, obstacles))
    coroutines.append(make_spaceship(coroutines, canvas, canvas_height, canvas_width))
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
