import lvgl as lv
import gc9a01
import lcd_bus
from machine import SPI, Pin
from micropython import const
from time import sleep

_WIDTH = const(240)
_HEIGHT = const(240)


_SPI_HOST = const(2)
_SPI_SCK = const(8)
_SPI_MOSI = const(9)
_SPI_MISO = const(-1)

_LCD_FREQ = const(80000000)
_LCD_DC = const(11)
_LCD_CS = const(12)
_LCD_RST = const(10)
_LCD_BACKLIGHT = const(13)

# Initialize LVGL
#lv.init()

# Initialize the SPI bus
spi_bus = SPI.Bus(
    host = _SPI_HOST,
    mosi = _SPI_MOSI,
    miso = _SPI_MISO,
    sck = _SPI_SCK
)

# Initialize the display bus
display_bus = lcd_bus.SPIBus(
    spi_bus = spi_bus,
    dc = _LCD_DC,
    cs = _LCD_CS,
    freq=_LCD_FREQ 
)

# Initialize the GC9A01 display driver
display = gc9a01.GC9A01(
    data_bus = display_bus,
    display_width = _WIDTH,
    display_height = _HEIGHT,
    reset_pin = _LCD_RST,
    reset_state = gc9a01.STATE_LOW,
    power_on_state = gc9a01.STATE_HIGH,
    backlight_pin=None,
    offset_x=0,
    offset_y=0,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True
)



import task_handler
th = task_handler.TaskHandler()

display.set_power(True)
display.init()
display.set_color_inversion(False)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)


# Create screen
scrn = lv.screen_active()
scrn.set_style_bg_color(lv.color_hex(0x000000), 0)  # Black background
scrn.set_scrollbar_mode(lv.SCROLLBAR_MODE.OFF)  # Disable scrollbars

# Create animated text label
animated_label = lv.label(scrn)
animated_label.set_text('SemiBlock')
animated_label.set_style_text_color(lv.color_hex(0x00ff00), 0)  # Green text

# Position the label initially at left edge
animated_label.set_pos(0, 120)

# Animation variables - keep within screen bounds
anim_x = 0
anim_direction = 1
anim_speed = 2

print('end')

import utime as time
time_passed = 1000

while True:
    start_time = time.ticks_ms()
    
    # Manual animation logic
    anim_x += anim_speed * anim_direction
    
    # Check boundaries and reverse direction - stay within screen
    if anim_x > 160:  # Right boundary (screen width - text width)
        anim_direction = -1  # Reverse direction
    elif anim_x < 0:  # Left boundary
        anim_direction = 1  # Reverse direction
    
    # Update label position
    animated_label.set_x(int(anim_x))
    
    time.sleep_ms(20)  # Animation frame delay
    lv.tick_inc(time_passed)
    lv.task_handler()
    end_time = time.ticks_ms()
    time_passed = time.ticks_diff(end_time, start_time)