from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import random, time

# Initialize display
display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)
display.set_backlight(1.0)

# Define colors
BG_COLOR = display.create_pen(0, 0, 0)
TEXT_COLOR = display.create_pen(0, 255, 0)
HEAD_COLOR = display.create_pen(180, 255, 180)

# Font and display settings
font_size = 2
char_width = 8 * font_size
char_height = 8 * font_size

cols = 320 // char_width
rows = 240 // char_height

# Generate character set
charset = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%&*"

# Track positions of falling characters for each column
drops = [random.randint(0, rows) for _ in range(cols)]

while True:
    display.set_pen(BG_COLOR)
    display.clear()

    for i in range(cols):
        x = i * char_width
        y = drops[i] * char_height

        # Draw trail
        for j in range(5):
            if 0 <= y - j * char_height < 240:
                char = random.choice(charset)
                brightness = 255 - j * 50
                brightness = max(brightness, 0)
                pen = display.create_pen(0, brightness, 0)
                display.set_pen(pen)
                display.text(char, x, y - j * char_height, -1, font_size)

        # Draw bright head
        if 0 <= y < 240:
            display.set_pen(HEAD_COLOR)
            display.text(random.choice(charset), x, y, -1, font_size)

        # Move drop down, reset to top randomly
        drops[i] += 1
        if drops[i] * char_height > 240 or random.random() > 0.95:
            drops[i] = 0

    display.update()
    time.sleep(0.05)
