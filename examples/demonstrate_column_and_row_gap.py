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

def row_gap_anim(obj, v):
    obj.set_style_pad_row(v, 0)

def column_gap_anim(obj, v):
    obj.set_style_pad_column(v, 0)

#
# Demonstrate column and row gap
#

# 60x60 cells
col_dsc = [60, 60, 60, lv.GRID_TEMPLATE_LAST]
row_dsc = [40, 40, 40, lv.GRID_TEMPLATE_LAST]

# Create a container with grid
cont = lv.obj(scr)
cont.set_size(240, 240)
cont.center()
cont.set_grid_dsc_array(col_dsc, row_dsc)

for i in range(9):
    col = i % 3
    row = i // 3

    obj = lv.obj(cont)
    obj.set_grid_cell(lv.GRID_ALIGN.STRETCH, col, 1,
                      lv.GRID_ALIGN.STRETCH, row, 1)
    label = lv.label(obj)
    label.set_text("{:d},{:d}".format(col, row))
    label.center()

    a_row = lv.anim_t()
    a_row.init()
    a_row.set_var(cont)
    a_row.set_values(0, 10)
    a_row.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    a_row.set_time(500)
    a_row.set_playback_time(500)
    a_row. set_custom_exec_cb(lambda a,val: row_gap_anim(cont,val))
    lv.anim_t.start(a_row)

    a_col = lv.anim_t()
    a_col.init()
    a_col.set_var(cont)
    a_col.set_values(0, 10)
    a_col.set_repeat_count(lv.ANIM_REPEAT_INFINITE)
    a_col.set_time(500)
    a_col.set_playback_time(500)
    a_col. set_custom_exec_cb(lambda a,val: column_gap_anim(cont,val))
    lv.anim_t.start(a_col)


import task_handler
th = task_handler.TaskHandler()
