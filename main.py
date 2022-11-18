import curses
import time

import timeline
from timeline import change_current_year, show_year

from spaceship import make_spaceship
from stars import make_stars
from space_garbage import fill_orbit_with_garbage


def draw(canvas):
    canvas.border()
    curses.curs_set(False)
    canvas.nodelay(True)
    canvas_height, canvas_width = canvas.getmaxyx()
    timeline.coroutines.append(show_year(canvas, canvas_height))
    timeline.coroutines.extend(make_stars(canvas, canvas_height, canvas_width))
    timeline.coroutines.append(make_spaceship(canvas, canvas_height, canvas_width))
    timeline.coroutines.append(fill_orbit_with_garbage(canvas, canvas_width))
    timeline.coroutines.append(change_current_year())
    while True:
        for coroutine in timeline.coroutines.copy():
            try:
                coroutine.send(None)
            except StopIteration:
                timeline.coroutines.remove(coroutine)
        canvas.refresh()
        time.sleep(1)


if __name__ == '__main__':
    curses.update_lines_cols()
    curses.wrapper(draw)
