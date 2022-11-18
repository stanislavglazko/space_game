from async_tools import sleep
from curses_tools import draw_frame, get_frame_size
from settings import GAME_OVER_FRAME, PATH_TO_ANIMATIONS


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
