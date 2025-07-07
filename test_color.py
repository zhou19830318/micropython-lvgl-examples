import lvgl as lv
import gc9a01
import lcd_bus
from machine import SPI, Pin
from micropython import const
import task_handler

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
display.set_power(True)
display.init()
display.set_color_inversion(False)
display.set_rotation(lv.DISPLAY_ROTATION._90)
display.set_backlight(100)

th = task_handler.TaskHandler()

scrn = lv.screen_active()

tabview = lv.tabview(scrn)
tabview.set_tab_bar_size(30)

tab1 = tabview.add_tab("SemiBlock")
tab2 = tabview.add_tab("Multimeter")
tab3 = tabview.add_tab("Oscilloscope")

# Test colors
colors = [
    (lv.color_hex(0xFF0000), "Red"),  # Pure red
    (lv.color_hex(0x00FF00), "Green"),  # Pure green
    (lv.color_hex(0x0000FF), "Blue"),  # Pure blue
    (lv.color_hex(0xFFFFFF), "White"),  # White
    (lv.color_hex(0x000000), "Black")   # Black
]
for i, (color, name) in enumerate(colors):
    rect = lv.obj(tab1)
    rect.set_size(30, 30)
    rect.set_style_bg_color(color, 0)
    rect.set_style_bg_opa(255, 0)
    rect.align(lv.ALIGN.TOP_LEFT, 10, 10 + i * 35)
    label = lv.label(tab1)
    label.set_text(name)
    label.align_to(rect, lv.ALIGN.OUT_RIGHT_MID, 10, 0)
