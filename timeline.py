from async_tools import sleep
from curses_tools import draw_frame
from game_scenario import PHRASES
from settings import speed_of_change_of_the_current_year, start_year

current_year = start_year

coroutines = []

obstacles = []
obstacles_in_last_collisions = []


async def change_current_year():
    global current_year
    while True:
        current_year += speed_of_change_of_the_current_year
        await sleep()


async def show_year(canvas, canvas_height):
    place_for_showing_year = canvas.derwin(canvas_height - 1, 0)
    while True:
        current_year_frame = get_current_year_frame()
        draw_frame(place_for_showing_year, 0, 0, current_year_frame)
        place_for_showing_year.syncup()
        await sleep()
        draw_frame(place_for_showing_year, 0, 0, current_year_frame, negative=True)


def get_current_year_frame():
    global current_year
    rounded_current_year = int(current_year)
    if PHRASES.get(rounded_current_year):
        return f'{rounded_current_year}:  {PHRASES[rounded_current_year]}'
    return f'{rounded_current_year}'
