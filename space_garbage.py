import asyncio
import random

import timeline
from async_tools import sleep
from curses_tools import draw_frame, get_frame_size
from explosion import explode
from game_scenario import get_garbage_delay_tics
from obstacles import Obstacle
from settings import GARBAGE_FRAMES, PATH_TO_ANIMATIONS, first_year_with_garbage


async def fill_orbit_with_garbage(canvas, canvas_width):
    garbage_frames = get_garbage_frames()
    while True:
        if timeline.current_year >= first_year_with_garbage:
            timeline.coroutines.append(
                fly_garbage(
                    canvas,
                    random.randint(0, canvas_width),
                    random.choice(garbage_frames)
                )
            )
            await sleep(get_garbage_delay_tics(int(timeline.current_year)))
        else:
            await sleep()


def get_garbage_frames():
    frames = []
    for frame in GARBAGE_FRAMES:
        with open(f'{PATH_TO_ANIMATIONS}{frame}') as garbage_file:
            frame = garbage_file.read()
            frames.append(frame)
    return frames



async def fly_garbage(canvas, column, garbage_frame, speed=0.2):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    garbaga_height, garbage_width = get_frame_size(garbage_frame)

    row = 0
    
    obstacle = Obstacle(row, column, garbaga_height, garbage_width)
    timeline.obstacles.append(obstacle)
    while row < rows_number:
        if obstacle in timeline.obstacles_in_last_collisions:
            timeline.obstacles_in_last_collisions.remove(obstacle)
            await explode(canvas, row, column)
            return
        obstacle.row = row
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        if row >= rows_number:
            timeline.obstacles.remove(obstacle)
