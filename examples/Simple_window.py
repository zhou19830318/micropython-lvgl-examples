import lvgl as lv
import gc9a01
import lcd_bus
from machine import SPI, Pin
from micropython import const
import fs_driver

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


def event_handler(e):
    code = e.get_code()
    obj = e.get_target()
    if code == lv.EVENT.CLICKED:
        print("Button {:d} clicked".format(obj.get_child_id()))


win = lv.win(scr)
btn1 = win.add_button(lv.SYMBOL.LEFT, 40)
btn1.add_event_cb(event_handler, lv.EVENT.ALL, None)
win.add_title("A title")
btn2=win.add_button(lv.SYMBOL.RIGHT, 40)
btn2.add_event_cb(event_handler, lv.EVENT.ALL, None)
btn3 = win.add_button(lv.SYMBOL.CLOSE, 60)
btn3.add_event_cb(event_handler, lv.EVENT.ALL, None)

cont = win.get_content()  # Content can be added here
label = lv.label(cont)
label.set_text("""This is
a pretty
long text
to see how
the window
becomes
scrollable.


We need
quite some text
and we will
even put
some more
text to be
sure it
overflows.
""")


import task_handler
th = task_handler.TaskHandler()
