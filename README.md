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
   使用基于 1.24.0 版本、已集成 lvgl 和 gc9a01 驱动的固件。可参考 [lvgl-micropython](https://github.com/lvgl-micropython) 仓库进行编译。

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
   import fs_driver
   from display_driver import init_display
   import task_handler
   
   # Initialize LVGL
   lv.init()
   
   # Initialize display using the driver module
   display = init_display()
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
   label.set_pos(60, 20)
   
   
   sw = lv.switch(scr)
   sw.center()
   sw.add_state(lv.STATE.CHECKED)
   sw.add_event_cb(lambda e: sw_event_cb(e,label), lv.EVENT.VALUE_CHANGED, None)
   
   th = task_handler.TaskHandler()
   ```

3. 若需适配其他屏幕或主控，请根据实际硬件修改初始化部分。


## 参考链接

- [LVGL 官方文档](https://docs.lvgl.io/9.2/examples.html)
- [lvgl-micropython](https://github.com/lvgl-micropython/lvgl_micropython)
- [MicroPython 官方网站](https://micropython.org/)

## 贡献

如需更详细的驱动初始化说明或主控适配方案，可在 README 中进一步补充。如有其他定制化需求欢迎告知！
