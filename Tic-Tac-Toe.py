from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)       # Confirm / place symbol / restart
button_down = Button(6, invert=False)    # Move cursor forward
button_up = Button(22, invert=False)     # Move cursor backward

WIDTH, HEIGHT = display.get_bounds()

BLACK = display.create_pen(0, 0, 0)
WHITE = display.create_pen(255, 255, 255)
GREEN = display.create_pen(0, 255, 0)
RED = display.create_pen(255, 0, 0)
BLUE = display.create_pen(0, 0, 255)

cell_w = WIDTH // 3
cell_h = (HEIGHT - 40) // 3

grid = [' '] * 9
cursor = 0
current_player = 'X'
game_over = False
winner = None

def draw_board():
    display.set_pen(BLACK)
    display.clear()

    display.set_pen(WHITE)
    display.set_font("bitmap8")
    if not game_over:
        display.text(f"Turn: {current_player}", 10, 10, WIDTH, 2)
    else:
        msg = f"{winner} wins!" if winner else "Draw!"
        display.text(msg, 10, 10, WIDTH, 2)
        display.text("Press A to restart", 10, 30, WIDTH, 1)

    # Draw grid lines
    for i in range(1, 3):
        display.line(i * cell_w, 40, i * cell_w, HEIGHT)
        display.line(0, 40 + i * cell_h, WIDTH, 40 + i * cell_h)

    # Draw X and O
    for i, val in enumerate(grid):
        x = (i % 3) * cell_w
        y = 40 + (i // 3) * cell_h
        if val != ' ':
            display.set_pen(RED if val == 'X' else BLUE)
            display.text(val, x + cell_w // 2 - 8, y + cell_h // 2 - 8, WIDTH, 4)

    # Draw cursor as green rectangle around current cell
    if not game_over:
        cx = (cursor % 3) * cell_w
        cy = 40 + (cursor // 3) * cell_h
        display.set_pen(GREEN)
        display.rectangle(cx + 2, cy + 2, cell_w - 4, cell_h - 4)

    display.update()

def check_winner():
    global game_over, winner
    lines = [
        (0,1,2),(3,4,5),(6,7,8),   # rows
        (0,3,6),(1,4,7),(2,5,8),   # cols
        (0,4,8),(2,4,6)            # diagonals
    ]
    for a,b,c in lines:
        if grid[a] == grid[b] == grid[c] != ' ':
            winner = grid[a]
            game_over = True
            return
    if ' ' not in grid:
        winner = None
        game_over = True

def reset_game():
    global grid, current_player, cursor, game_over, winner
    grid = [' '] * 9
    current_player = 'X'
    cursor = 0
    game_over = False
    winner = None

draw_board()

while True:
    if button_down.is_pressed and not game_over:
        cursor = (cursor + 1) % 9  # Move cursor forward, wrap around
        draw_board()
        while button_down.is_pressed:
            time.sleep(0.01)

    if button_up.is_pressed and not game_over:
        cursor = (cursor - 1) % 9  # Move cursor backward, wrap around
        draw_board()
        while button_up.is_pressed:
            time.sleep(0.01)

    if button_a.is_pressed:
        if game_over:
            reset_game()
        else:
            if grid[cursor] == ' ':
                grid[cursor] = current_player
                check_winner()
                if not game_over:
                    current_player = 'O' if current_player == 'X' else 'X'
        draw_board()
        while button_a.is_pressed:
            time.sleep(0.01)

    time.sleep(0.01)
