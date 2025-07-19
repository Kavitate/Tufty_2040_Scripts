from picographics import PicoGraphics, DISPLAY_TUFTY_2040
from pimoroni import Button
import time
import jpegdec
import qrcode

display = PicoGraphics(display=DISPLAY_TUFTY_2040)
button_a = Button(7, invert=False)
button_b = Button(8, invert=False)
button_c = Button(9, invert=False)

WIDTH, HEIGHT = display.get_bounds()

# Custom color palette
COLOR_GREEN = display.create_pen(0, 255, 0)
COLOR_ORANGE = display.create_pen(255, 165, 0)
COLOR_RED = display.create_pen(255, 0, 0)
TEXT_COLOR_DEFAULT = display.create_pen(255, 0, 0)
BG_COLOR = display.create_pen(0, 0, 0)
FRAME_COLOR = display.create_pen(0, 0, 0)

# Badge info
NAME = "Kavitate"
ROLE = "Founder"
IMAGE_NAME = "smallpfp.jpg"

# Status messages mapped to buttons
status_map = {
    'A': ("Thriving", COLOR_GREEN),
    'B': ("Getting Drunk", COLOR_ORANGE),
    'C': ("Drunk", COLOR_RED),
}

# Start with default status text and color as original company name in red
current_status_text = "The Pirates' Plunder"
current_status_color = TEXT_COLOR_DEFAULT

BORDER_SIZE = 4
PADDING = 10
COMPANY_HEIGHT = 40

def draw_badge():
    display.set_pen(BG_COLOR)
    display.clear()

    # Draw background
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), HEIGHT - (BORDER_SIZE * 2))

    # Draw status background box with current status color
    display.set_pen(current_status_color)
    display.rectangle(BORDER_SIZE, BORDER_SIZE, WIDTH - (BORDER_SIZE * 2), COMPANY_HEIGHT)

    # Draw centered status text in BLACK on top of the colored background
    display.set_pen(BG_COLOR)  # Black pen for text
    display.set_font("bitmap6")
    company_scale = 2
    status_text_width = display.measure_text(current_status_text, scale=company_scale)
    status_text_x = (WIDTH - status_text_width) // 2
    status_text_y = BORDER_SIZE + (COMPANY_HEIGHT - 8 * company_scale) // 2
    display.text(current_status_text, status_text_x, status_text_y, WIDTH, company_scale)


    # Draw centered name below status
    display.set_pen(TEXT_COLOR_DEFAULT)
    display.set_font("bitmap8")
    name_scale = 5
    name_text_width = display.measure_text(NAME, scale=name_scale)
    name_text_x = (WIDTH - name_text_width) // 2
    name_text_y = BORDER_SIZE + COMPANY_HEIGHT + 10
    display.text(NAME, name_text_x, name_text_y, WIDTH, name_scale)

def show_photo():
    j = jpegdec.JPEG(display)
    j.open_file(IMAGE_NAME)

    img_size = 120
    frame_size = img_size + (BORDER_SIZE * 2)
    img_x = (WIDTH - frame_size) // 2
    img_y = HEIGHT - frame_size - PADDING

    display.set_pen(FRAME_COLOR)
    display.rectangle(img_x, img_y, frame_size, frame_size)

    j.decode(img_x + BORDER_SIZE, img_y + BORDER_SIZE)

def measure_qr_code(size, code):
    w, h = code.get_size()
    module_size = int(size / w)
    return module_size * w, module_size

def draw_qr_code(ox, oy, size, code):
    size, module_size = measure_qr_code(size, code)
    display.set_pen(TEXT_COLOR_DEFAULT)
    display.rectangle(ox, oy, size, size)
    display.set_pen(FRAME_COLOR)
    for x in range(size):
        for y in range(size):
            if code.get_module(x, y):
                display.rectangle(ox + x * module_size, oy + y * module_size, module_size, module_size)

def show_qr():
    display.set_pen(BG_COLOR)
    display.clear()

    code = qrcode.QRCode()
    code.set_text("https://discord.com/invite/thepirates")

    size, module_size = measure_qr_code(HEIGHT, code)
    left = int((WIDTH // 2) - (size // 2))
    top = int((HEIGHT // 2) - (size // 2))
    draw_qr_code(left, top, HEIGHT, code)

def update_status_by_button():
    global current_status_text, current_status_color
    if button_a.is_pressed:
        current_status_text, current_status_color = status_map['A']
        return True
    elif button_b.is_pressed:
        current_status_text, current_status_color = status_map['B']
        return True
    elif button_c.is_pressed:
        current_status_text, current_status_color = status_map['C']
        return True
    return False

# Initialize mode and draw first badge + photo
badge_mode = "photo"
draw_badge()
show_photo()
display.update()

while True:
    # Update status text if any status button pressed
    if update_status_by_button():
        draw_badge()
        show_photo()
        display.update()
        time.sleep(0.3)  # debounce delay

    # Original toggle for badge_mode on button_c press
    if button_c.is_pressed and badge_mode == "photo":
        badge_mode = "qr"
        show_qr()
        display.update()
        time.sleep(1)
    elif button_c.is_pressed and badge_mode == "qr":
        badge_mode = "photo"
        draw_badge()
        show_photo()
        display.update()
        time.sleep(1)

    time.sleep(0.05)
