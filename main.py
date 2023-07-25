# import
# import UI
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox as mbox
import sv_ttk
from win32mica import MICAMODE, ApplyMica
import darkdetect
from ctypes import windll

# other import
from pathlib import Path
import random
import json
import unicodedata
import subprocess
import pyperclip
import webbrowser


# action
class PickerApp:
    def __init__(self):
        self.result = ""
        self.history_point = 0
        # load settings
        self.path = Path(__file__).resolve().parent
        windll.shcore.SetProcessDpiAwareness(1)
        with open("settings.json") as configure:
            cfg_list = configure.read()
            cfg_list = json.loads(cfg_list)
        self.list_path = "%s\\%s" % (self.path, cfg_list["path"])
        self.history_path = "%s\\history.txt" % self.path
        if cfg_list["mini_ui"]:
            self.ui_font = 1.5
        else:
            self.ui_font = 2
        if cfg_list["theme"] == "auto":
            if darkdetect.isDark():
                self.theme = "dark"
            else:
                self.theme = "light"
        else:
            self.theme = cfg_list["theme"]
        # creat a window

        self.root = tk.Tk()
        self.root.title("Picker")
        self.root.iconphoto(
            True, tk.PhotoImage(file="%s\\icon_%s.png" % (self.path, self.theme))
        )
        self.root.geometry(
            "%dx%d+%d+%d"
            % (
                1000,
                650,
                (self.root.winfo_screenwidth() - 1000) / 2,
                (self.root.winfo_screenheight() - 650) / 2,
            )
        )
        self.root.minsize(575, 375)

        # High DPI support
        self.root.tk.call(
            "tk", "scaling", windll.shcore.GetScaleFactorForDevice(0) / 75
        )

        # Fluent Design
        sv_ttk.set_theme(self.theme)
        self.root.update()
        if self.theme == "dark":
            ApplyMica(windll.user32.GetParent(self.root.winfo_id()), MICAMODE.LIGHT)
        stylesheet = ttk.Style()
        stylesheet.configure(
            "TLabelframe.Label",
            font=("Microsoft YaHei UI", int(self.ui_font * 5), "bold"),
        )
        stylesheet.configure(
            "Accent.TButton",
            font=(
                "Microsoft YaHei UI",
                int(self.ui_font * 7.5),
            ),
        )
        stylesheet.configure(
            "TButton",
            font=(
                "Microsoft YaHei UI",
                int(self.ui_font * 6.25),
            ),
        )
        stylesheet.configure(
            "TLabel", font=("Microsoft YaHei UI", int(self.ui_font * 7.5))
        )
        stylesheet.configure(
            "TMenubutton",
            highlightbackground="white",
            highlightthickness=0,
            font=("Microsoft YaHei UI", int(self.ui_font * 6.25)),
        )
        # st5=ttk.Style()
        # st5.configure(
        #     "TNotebook.Tab", font=("Microsoft YaHei UI", self.ui_font, "bold")
        # )

        # UI

        self.frame_menu = ttk.LabelFrame(self.root, text="工具栏")
        self.frame_main = tk.Frame(self.root)
        self.frame_toolbar = tk.Frame(self.frame_main)

        # menu

        # file
        self.mb_file = ttk.Menubutton(
            self.frame_menu, text="文件", width=int(self.ui_font * 2)
        )
        self.menu_file = tk.Menu(
            self.mb_file, font=("Microsoft YaHei UI", int(self.ui_font * 6.25))
        )
        self.menu_file.add_command(
            label="打开名单文件",
            command=lambda: subprocess.call('explorer "%s"' % self.list_path),
        )
        self.menu_file.add_command(
            label="打开历史记录文件",
            command=lambda: subprocess.call(
                'explorer "%s\\%s"' % (self.path, "history.txt")
            ),
        )
        self.menu_file.add_separator()
        # self.menu_file.add_command(label="打开设置(UI)")
        self.menu_file.add_command(
            label="打开设置(JSON)",
            command=lambda: subprocess.call(
                'explorer "%s\\%s"' % (self.path, "settings.json")
            ),
        )
        self.mb_file.config(menu=self.menu_file)
        self.mb_file.bind("<Return>", lambda e: self.menu_ev(e, "mb_file", "menu_file"))
        self.mb_file.bind_all(
            "<Control-KeyPress-1>", lambda e: self.menu_ev(e, "mb_file", "menu_file")
        )
        # edit
        self.mb_edit = ttk.Menubutton(
            self.frame_menu, text="编辑", width=int(self.ui_font * 2)
        )
        self.menu_edit = tk.Menu(
            self.mb_file, font=("Microsoft YaHei UI", int(self.ui_font * 6.25))
        )
        self.menu_edit.add_command(label="人数 +1", command=lambda: self.num_add(1))
        self.menu_edit.add_command(label="人数 -1", command=lambda: self.num_add(-1))
        self.menu_edit.add_separator()
        self.menu_edit.add_command(label="人数 +5", command=lambda: self.num_add(5))
        self.menu_edit.add_command(label="人数 -5", command=lambda: self.num_add(-5))
        self.mb_edit.config(menu=self.menu_edit)
        self.mb_edit.bind("<Return>", lambda e: self.menu_ev(e, "mb_edit", "menu_edit"))
        self.mb_edit.bind_all(
            "<Control-KeyPress-2>", lambda e: self.menu_ev(e, "mb_edit", "menu_edit")
        )
        # action
        self.mb_action = ttk.Menubutton(
            self.frame_menu, text="操作", width=int(self.ui_font * 2)
        )
        self.menu_action = tk.Menu(
            self.mb_file, font=("Microsoft YaHei UI", int(self.ui_font * 6.25))
        )
        self.menu_action.add_command(
            label="抽取", command=lambda: self.start(int(self.var_num.get()))
        )
        self.menu_action.add_separator()
        self.menu_action.add_command(label="抽取 x1", command=lambda: self.start(1))
        self.menu_action.add_command(label="抽取 x2", command=lambda: self.start(2))
        self.menu_action.add_command(label="抽取 x5", command=lambda: self.start(5))
        self.menu_action.add_command(label="抽取 x10", command=lambda: self.start(10))
        self.menu_action.add_separator()
        self.menu_action.add_command(label="撤销", command=lambda: self.undo(1))
        self.menu_action.add_command(label="重做", command=lambda: self.undo(-1))
        self.mb_action.config(menu=self.menu_action)
        self.mb_action.bind(
            "<Return>", lambda e: self.menu_ev(e, "mb_action", "menu_action")
        )
        self.mb_action.bind_all(
            "<Control-KeyPress-3>",
            lambda e: self.menu_ev(e, "mb_action", "menu_action"),
        )
        # about
        self.mb_about = ttk.Menubutton(
            self.frame_menu, text="帮助", width=int(self.ui_font * 2)
        )
        self.menu_about = tk.Menu(
            self.mb_file, font=("Microsoft YaHei UI", int(self.ui_font * 6.25))
        )
        self.menu_about.add_command(
            label="在线查看本项目",
            command=lambda: webbrowser.open("https://github.com/I-AM-A-NOOB/Picker"),
        )
        self.menu_about.add_command(label="关于", command=self.about)
        self.mb_about.config(menu=self.menu_about)
        self.mb_about.bind(
            "<Return>", lambda e: self.menu_ev(e, "mb_about", "menu_about")
        )
        self.mb_about.bind_all(
            "<Control-KeyPress-4>", lambda e: self.menu_ev(e, "mb_about", "menu_about")
        )

        # objects

        self.name_bar = ttk.Scrollbar(self.frame_main)
        self.name = tk.Text(
            self.frame_main,
            relief="flat",
            font=("黑体", 40),
            yscrollcommand=self.name_bar.set,
        )
        if self.theme == "dark":
            self.name.config(bg="black", fg="white")
        else:
            self.name.config(bg="white", fg="black")
        self.name_menu = tk.Menu(
            self.name, font=("Microsoft YaHei UI", int(self.ui_font * 6.25))
        )
        self.name_menu.add_command(
            label="复制全部（空格分隔）",
            command=lambda: pyperclip.copy(" ".join(self.result[0 : len(self.result)])),
        )
        self.name_menu.add_command(
            label="复制全部（换行符分隔）",
            command=lambda: pyperclip.copy(
                "\n".join(self.result[0 : len(self.result)])
            ),
        )
        self.name_menu.add_command(
            label="清空", command=lambda: self.name.delete(1.0, tk.END)
        )
        self.name_menu.add_separator()
        self.name_menu.add_command(label="撤销", command=lambda: self.undo(1))
        self.name_menu.add_command(label="重做", command=lambda: self.undo(-1))
        self.name.bind("<Button-3>", self.click_ev)
        self.go = ttk.Button(
            self.frame_toolbar,
            text="天选之子",
            width=10,
            command=lambda: self.start(int(self.var_num.get())),
            style="Accent.TButton",
        )
        self.go.bind_all("<Control-Return>", self.start_ev)
        self.go.bind("<Return>", self.start_ev)
        self.tip = ttk.Label(self.frame_toolbar, text="人数：")
        self.var_num = tk.StringVar()
        self.var_num.set("1")
        self.num = ttk.Spinbox(
            self.frame_toolbar,
            textvariable=self.var_num,
            font=("Microsoft YaHei UI", int(self.ui_font * 6.25)),
            from_=0,
            to=float("inf"),
            validate="all",
            validatecommand=self.num_input,
            command=self.num_check,
        )
        self.name.bind_all("<Control-]>", lambda e: self.num_add_ev(e, 1))
        self.name.bind_all("<Control-[>", lambda e: self.num_add_ev(e, -1))
        self.name.bind("<KeyPress-Up>", lambda e: self.num_add_ev(e, 1))
        self.name.bind("<KeyPress-Down>", lambda e: self.num_add_ev(e, -1))
        self.edit = ttk.Button(
            self.frame_toolbar,
            width=7,
            text="编辑名单",
            command=lambda: subprocess.call('explorer "%s"' % self.list_path),
        )

        # place

        self.frame_menu.pack(side="top", fill="x", ipadx=10, ipady=10, padx=5, expand=1)
        self.mb_file.pack(side="left", fill="none", padx=7.5, expand=0)
        self.mb_edit.pack(side="left", fill="none", padx=7.5, expand=0)
        self.mb_action.pack(side="left", fill="none", padx=7.5, expand=0)
        self.mb_about.pack(side="left", fill="none", padx=7.5, expand=0)

        self.frame_toolbar.pack(side="bottom", fill="none", ipadx=5, ipady=5, expand=0)
        self.go.pack(side="top", fill="none", pady=2, expand=0)
        self.tip.pack(side="left", fill="none", expand=0, padx=10)
        self.edit.pack(side="right", fill="none", expand=0, padx=10)
        self.num.pack(side="left", fill="x", pady=5, expand=1)

        self.frame_main.pack(side="top", fill="both", expand=1)
        self.name_bar.pack(side="right", fill="y", pady=5, expand=0)
        self.name_bar.config(command=self.name.yview)
        self.name.pack(side="left", padx=5, pady=5, fill="both", expand=1)

        self.go.focus_set()
        self.root.bind("<Configure>", self.direct_ev)
        self.root.mainloop()

    def start_ev(self, event):
        self.start(int(self.var_num.get()))

    def click_ev(self, event):
        self.name_menu.post(event.x_root, event.y_root)

    def menu_ev(self, event, name: str, menu_name: str):
        exec(
            """self.%s.post(
                self.root.winfo_x() + self.%s.winfo_x() + 14,
                self.root.winfo_y()+ self.%s.winfo_y()+ self.%s.winfo_height()+ 38,
            )"""
            % (menu_name, name, name, name)
        )

    def direct_ev(self, event):
        self.direct()

    def num_add_ev(self, event, m: int):
        self.num_add(m)

    def file_read(self):
        try:
            with open(self.list_path, "r", encoding="utf-8") as names:
                namelist = tuple(names.readlines())
                return namelist
        except FileNotFoundError:
            with open(self.list_path, "w", encoding="utf-8") as names:
                names.writelines(["Alice\n", "Bob\n", "Carol\n", "Dan\n"])
            mbox.showwarning(title="warning", message="您可能还未创建名单\n已自动生成")
            return "Alice", "Bob", "Carol", "Dan"

    def history_read(self):
        try:
            with open(self.history_path, "r", encoding="utf-8") as names:
                namelist = tuple(names.readlines())
                return namelist
        except FileNotFoundError:
            with open(self.history_path, "w", encoding="utf-8") as names:
                names.writelines([])
            return ()

    def str_fmt(self, string: str):
        if string[len(string) - 1] == "\n" or string[len(string) - 1] == "\0":
            return_string = string[0 : (len(string) - 1)]
            return self.str_fmt(return_string)
        else:
            return string

    def start(self, num: int):
        self.history_point = 0
        self.num_check()
        n_list_source = self.file_read()
        h_list_source = self.history_read()
        n_list = []
        h_list = []
        for i in n_list_source:
            n_list += self.str_fmt(i).split(" ")
        for i in h_list_source:
            h_list += self.str_fmt(i).split(" ")
        h_list = h_list[len(h_list) - len(n_list) + num + 1 : len(h_list)]
        for i in h_list:
            try:
                n_list.remove(i)
            except ValueError:
                pass
        self.result = []
        num_result = random.sample(range(0, len(n_list)), num)
        num_result.sort()
        for i in num_result:
            self.result.append(n_list[i])
        with open(self.history_path, "a", encoding="utf-8") as history:
            history.write("%s\n" % " ".join(self.result))
        self.direct()

    def num_add(self, a: int):
        self.var_num.set(str(int(self.var_num.get()) + a))
        self.num_check()

    def num_input(self):
        try:
            self.num_check()
        except ValueError:
            if str(self.num.focus_get()) != ".!frame.!frame.!spinbox":
                self.var_num.set("1")
        return True

    def num_check(self):
        length = len(self.file_read())
        if int(self.var_num.get()) > length - 1:
            self.var_num.set(str(length - 1))
        if int(self.var_num.get()) < 1:
            self.var_num.set("1")

    def str_width(self, c: str):
        length = 0
        for i in c:
            if unicodedata.east_asian_width(i) in ("F", "W", "A"):
                length += 2
            else:
                length += 1
        return length

    def direct(self):
        width = self.root.winfo_width() - 45
        result_width = list(self.str_width(i) + 1 for i in self.result)
        width_line = 0
        line = 0
        display = []
        i = 0
        while i < len(self.result):
            if width_line + 34 * (result_width[i] + 1) > width:
                display.append(" ".join(self.result[line:i]))
                width_line = 0
                line = i
            width_line += 34 * (result_width[i] + 1)
            i += 1

        display.append(" ".join(self.result[line : i + 1]))
        self.name.delete(1.0, tk.END)
        for i in display:
            self.name.insert("insert", i)
            self.name.insert("insert", "\n")

    def undo(self, num: int):
        try:
            h_list = list(self.history_read())
            self.history_point += num
            self.result = []
            self.result.append(h_list[(len(h_list) - self.history_point - 1)])
            self.direct()
        except IndexError:
            pass

    def settings(self):
        set = tk.Tk()
        set.mainloop()

    def about(self):
        mbox.showinfo(title="about", message="By I-AM-A-NOOB\n感谢老师对我的培养")


if __name__ == "__main__":
    # creat window
    picker = PickerApp()
