from picographics import PicoGraphics, DISPLAY_TUFTY_2040, PEN_RGB332
import math, time

display = PicoGraphics(display=DISPLAY_TUFTY_2040, pen_type=PEN_RGB332, rotate=180)
display.set_backlight(1.0)

# Set red color for text and dark grey background
TEXT_COLOR = display.create_pen(255, 0, 0)
SHADOW_COLOR = display.create_pen(0, 0, 0)
BG_COLOR = display.create_pen(0, 0, 0)

message = "Kavitate"
text_size =6
char_spacing = text_size * 5.5
message_width = display.measure_text(message, text_size)
start_x = (320 - message_width) // 2  # Centered horizontally

while True:
    t = time.ticks_ms() / 1000.0

    display.set_pen(BG_COLOR)
    display.clear()

    # Draw each character with vertical sine wave
    for i in range(len(message)):
        cx = int(start_x + i * char_spacing)
        cy = int(80 + math.sin(t * 5 + i * 0.5) * 20)  # wave in place

        # draw shadow
        display.set_pen(SHADOW_COLOR)
        display.text(message[i], cx + 2, cy + 2, -1, text_size)

        # draw red text
        display.set_pen(TEXT_COLOR)
        display.text(message[i], cx, cy, -1, text_size)

    display.update()
