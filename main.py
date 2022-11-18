import curses
import time

from timeline import change_current_year, show_year

from spaceship import make_spaceship
from stars import make_stars
from space_garbage import fill_orbit_with_garbage


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    coroutines = []
    canvas_height, canvas_width = canvas.getmaxyx()
    coroutines.append(show_year(canvas, canvas_height))
    coroutines.extend(make_stars(canvas, canvas_height, canvas_width))
    coroutines.append(make_spaceship(coroutines, canvas, canvas_height, canvas_width))
    coroutines.append(fill_orbit_with_garbage(coroutines, canvas, canvas_width))
    coroutines.append(change_current_year())
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
