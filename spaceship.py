import time

from itertools import cycle

import timeline

from async_tools import sleep
from curses_tools import draw_frame, get_frame_size, read_controls
from fire import fire
from game_over import show_game_over
from physics import update_speed
from settings import (
    PATH_TO_ANIMATIONS,
    SHIP_FRAMES,
    first_year_with_weapon,
)


async def run_spaceship(canvas, canvas_height, canvas_width):
    ship_frame1, ship_frame2 = get_ship_frames()
    ships_height, ships_width = get_frame_size(ship_frame1)
    ship_frames = [ship_frame1, ship_frame1, ship_frame2, ship_frame2]

    start_row, start_column = get_start_point(canvas_height, canvas_width, ships_height, ships_width)
    row, column = start_row, start_column

    row_speed = column_speed = 0
    iterator = cycle(ship_frames)
    current_ship_frame = next(iterator)

    for frame in iterator:
        for obstacle in timeline.obstacles:
            if obstacle.has_collision(row, column):
                draw_frame(canvas, row, column, current_ship_frame, negative=True)
                timeline.coroutines.append(show_game_over(canvas, start_row, start_column))
                return
        rows_direction, columns_direction, space_pressed = read_controls(canvas)
        draw_frame(canvas, row, column, current_ship_frame, negative=True)
        row_speed, column_speed = update_speed(row_speed, column_speed, rows_direction, columns_direction)
        if row + row_speed > 0 and row + row_speed + ships_height < canvas_height:
            row += row_speed
        if column + column_speed > 0 and column + column_speed + ships_width < canvas_width:
            column += column_speed
        if space_pressed and timeline.current_year >= first_year_with_weapon:
            timeline.coroutines.append(fire(canvas, row, column + ships_width // 2, rows_speed=-1))
        draw_frame(canvas, row, column, frame)
        current_ship_frame = frame
        time.sleep(0)
        await sleep()


def get_ship_frames():
    with open(f'{PATH_TO_ANIMATIONS}{SHIP_FRAMES[0]}', 'r') as frame1:
        ship_frame1 = frame1.read()
    with open(f'{PATH_TO_ANIMATIONS}{SHIP_FRAMES[1]}', 'r') as frame2:
        ship_frame2 = frame2.read()
    return ship_frame1, ship_frame2


def get_start_point(canvas_height, canvas_width, ships_height, ships_width):
    start_row = (canvas_height // 2) - (ships_height // 2)
    start_column = (canvas_width // 2) - (ships_width // 2)
    return start_row, start_column
