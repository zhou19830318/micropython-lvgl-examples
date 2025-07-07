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

def anim_x_cb(label, v):
    label.set_x(v)

def sw_event_cb(e,label):
    sw = e.get_target()

    if sw.has_state(lv.STATE.CHECKED):
        a = lv.anim_t()
        a.init()
        a.set_var(label)
        a.set_values(label.get_x(), 100)
        a.set_time(500)
        a.set_path_cb(lv.anim_t.path_overshoot)
        a.set_custom_exec_cb(lambda a,val: anim_x_cb(label,val))
        lv.anim_t.start(a)
    else:
        a = lv.anim_t()
        a.init()
        a.set_var(label)
        a.set_values(label.get_x(), -label.get_width())
        a.set_time(500)
        a.set_path_cb(lv.anim_t.path_ease_in)
        a.set_custom_exec_cb(lambda a,val: anim_x_cb(label,val))
        lv.anim_t.start(a)

#
# Start animation on an event
#

label = lv.label(scr)
label.set_text("Hello animations!")
label.set_pos(60, 10)


sw = lv.switch(scr)
sw.center()
sw.add_state(lv.STATE.CHECKED)
sw.add_event_cb(lambda e: sw_event_cb(e,label), lv.EVENT.VALUE_CHANGED, None)


import task_handler
th = task_handler.TaskHandler()