import asyncio
from obstacles import Obstacle
from tools import draw_frame, get_frame_size



async def fly_garbage(obstacles, canvas, column, garbage_frame, speed=0.5):
    """Animate garbage, flying from top to bottom. Сolumn position will stay same, as specified on start."""
    rows_number, columns_number = canvas.getmaxyx()

    column = max(column, 0)
    column = min(column, columns_number - 1)

    garbaga_height, garbage_width = get_frame_size(garbage_frame)

    row = 0
    
    obstacle = Obstacle(row, column, garbaga_height, garbage_width)
    obstacles.append(obstacle)
    while row < rows_number:
        obstacle.row = row
        draw_frame(canvas, row, column, garbage_frame)
        await asyncio.sleep(0)
        draw_frame(canvas, row, column, garbage_frame, negative=True)
        row += speed
        if row >= rows_number:
            obstacles.remove(obstacle)
