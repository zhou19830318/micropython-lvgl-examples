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


scrn = lv.screen_active()

# Fallback: Create a simple pattern using objects
# Create colorful rectangles as objects instead
colors = [0xFF0000, 0x00FF00, 0x0000FF, 0xFFFF00, 0xFF00FF, 0x00FFFF]

for i, color in enumerate(colors):
    rect = lv.obj(scrn)
    rect.set_size(40, 40)
    
    # Position in 3x2 grid
    x = (i % 3) * 50 - 50  # Center around screen
    y = (i // 3) * 50 - 25
    rect.align(lv.ALIGN.CENTER, x, y)
    
    # Set color
    rect.set_style_bg_color(lv.color_hex(color), 0)
    rect.set_style_bg_opa(lv.OPA.COVER, 0)
    rect.set_style_border_width(0, 0)  # No border

# Add a label to show status
label1 = lv.label(scrn)
label1.set_text("Colorful Pattern (Fallback)")
label1.align(lv.ALIGN.TOP_MID, 0, 10)

sleep(2)