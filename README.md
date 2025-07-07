# micropython-lvgl-examples

本项目提供基于 [lvgl-micropython](https://github.com/lvgl-micropython/lvgl_micropython)编译环境下，适配 gc9a01 圆形显示屏的 LVGL 9.2.2 示例代码，适用于嵌入式开发者快速体验与学习 LVGL 图形界面开发。

## 项目说明

- **LVGL 版本**：9.2.2
- **MicroPython 版本**：基于 1.24.0 编译
- **显示屏驱动**：gc9a01
- **硬件平台**：支持 MicroPython 的主控板（如 ESP32S3）

## 目录结构

```
micropython-lvgl-examples/
├── examples/        # LVGL 控件与功能演示代码
├── images/          # 示例用图片资源
├── README.md        # 项目说明文件
└── ...              # 其他相关文件
```

## 环境准备

1. **MicroPython 固件**  
   使用基于 1.24.0 版本、已集成 lvgl 和 gc9a01 驱动的固件。可参考 [lv_binding_micropython](https://github.com/lvgl/lv_binding_micropython) 仓库进行编译。

2. **硬件连接**  
   按照 gc9a01 屏幕和主控板的硬件手册完成连线。

3. **依赖库准备**  
   - lvgl-micropython
   - gc9a01

## 快速开始

1. 将本项目中的 `examples/`、`images/` 目录和所需驱动文件上传到开发板。
2. 在 REPL 或 main.py 中运行示例（如）：

   ```python
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
   
   def event_handler(evt):
       code = evt.get_code()
   
       if code == lv.EVENT.CLICKED:
               print("Clicked event seen")
       elif code == lv.EVENT.VALUE_CHANGED:
           print("Value changed seen")
   
   # create a simple button
   btn1 = lv.button(scr)
   
   # attach the callback
   btn1.add_event_cb(event_handler,lv.EVENT.ALL, None)
   
   btn1.align(lv.ALIGN.CENTER,0,-40)
   label=lv.label(btn1)
   label.set_text("Button")
   
   # create a toggle button
   btn2 = lv.button(scr)
   
   # attach the callback
   #btn2.add_event_cb(event_handler,lv.EVENT.VALUE_CHANGED,None)
   btn2.add_event_cb(event_handler,lv.EVENT.ALL, None)
   
   btn2.align(lv.ALIGN.CENTER,0,40)
   btn2.add_flag(lv.obj.FLAG.CHECKABLE)
   btn2.set_height(lv.SIZE_CONTENT)
   
   label=lv.label(btn2)
   label.set_text("Toggle")
   label.center()
   
   import task_handler
   th = task_handler.TaskHandler()
   ```

3. 若需适配其他屏幕或主控，请根据实际硬件修改初始化部分。


## 参考链接

- [LVGL 官方文档](https://docs.lvgl.io/9.2/examples.html)
- [lvgl-micropython](https://github.com/lvgl-micropython/lvgl_micropython)
- [MicroPython 官方网站](https://micropython.org/)

## 贡献

如需更详细的驱动初始化说明或主控适配方案，可在 README 中进一步补充。如有其他定制化需求欢迎告知！
