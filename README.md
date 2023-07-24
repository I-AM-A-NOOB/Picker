# Picker

对希沃班级优化大师“随机抽选”功能简单替代
谨献给我的老师

## 简介

使用Python编写，理论上支持Windows10/11

注：*仅在Windows11上进行过测试，由于罕有人用Mac/Linux上课故不作支持*

## 文件说明

|文件|说明|
|-|-|
|icon_dark.png|窗口图标（暗）|
|icon_light.png|窗口图标（亮）|
|icon.ico|程序图标|
|sarasa-mono.ttf|字体|
|main.py|主程序源代码|
|settings.json|设置|
|namelist.txt|名单，可在设置中调整|
|LICENSE|MIT许可证|
|README.md|说明/关于/感谢|

## 主程序依赖库

|依赖|协议|
|-|-|
|sv_ttk|MIT|
|win32mica|MIT|
|darkdetect|BSD|
|pyglet|BSD|
|pyperclip|BSD|

## TODO

### UI

- [x] Fluent UI
- [x] 按钮绑定函数
- [x] 结果自适应窗体宽度
- [ ] 更多快捷键绑定
- [ ] 设置界面
- [ ] 更多布局选项

### Other feature

- [x] 历史记录回溯
- [ ] 截图

### Function

- [ ] 将自定义组件独立与"PickerAPP"类
- [ ] 对函数进行整理以及补充注释
