import lvgl as lv
import gc9a01
import lcd_bus
from machine import SPI, Pin
from micropython import const
import fs_driver
import sys

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


# Initialize display
display.init()

scr = lv.screen_active()

# Create an image from the png file
try:
    with open('img_caret_down.png','rb') as f:
        png_data = f.read()
except:
    print("Could not find img_caret_down.png")
    sys.exit()

img_caret_down_argb = lv.image_dsc_t({
  'data_size': len(png_data),
  'data': png_data
})

def event_cb(e):
    dropdown = e.get_target()
    option = " "*64 # should be large enough to store the option
    dropdown.get_selected_str(option, len(option))
    print(option.strip() +" is selected")
#
# Create a menu from a drop-down list and show some drop-down list features and styling
#

# Create a drop down list
dropdown = lv.dropdown(scr)
dropdown.align(lv.ALIGN.CENTER, 10, 10)
dropdown.set_options("\n".join([
    "New project",
    "New file",
    "Open project",
    "Recent projects",
    "Preferences",
    "Exit"]))

# Set a fixed text to display on the button of the drop-down list
dropdown.set_text("Menu")

# Use a custom image as down icon and flip it when the list is opened
# LV_IMG_DECLARE(img_caret_down)
dropdown.set_symbol(img_caret_down_argb)
dropdown.set_style_transform_rotation(1800, lv.PART.INDICATOR | lv.STATE.CHECKED)

# In a menu we don't need to show the last clicked item
dropdown.set_selected_highlight(False)

dropdown.add_event_cb(event_cb, lv.EVENT.VALUE_CHANGED, None)

import task_handler
th = task_handler.TaskHandler()