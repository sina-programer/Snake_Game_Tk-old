import sys
import webbrowser
import tkinter as tk
from tkinter import simpledialog, colorchooser, messagebox

from database import User

is_windows = sys.platform == 'win32'
if is_windows:
    import winsound


class BaseDialog(simpledialog.Dialog):
    def __init__(self, parent, title, app=None):
        if app:
            self.app = app

        super(BaseDialog, self).__init__(parent, title)

    def buttonbox(self):
        pass


class BestScoresDialog(BaseDialog):
    def __init__(self, parent, app):
        super(BestScoresDialog, self).__init__(parent, 'Best scores', app)

    def body(self, frame):
        list_box = tk.Listbox(frame)
        list_box.pack(side=tk.LEFT)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        for user in User.select().order_by(User.best_score):
            list_box.insert(tk.END, f' {user.name}: {user.best_score}')

        list_box.configure(yscrollcommand=scrollbar.set)
        scrollbar.configure(command=list_box.yview)
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame


class SettingDialog(BaseDialog):
    def __init__(self, parent, app):
        self.need_restart = False
        self.level_var = tk.IntVar()
        self.user_var = tk.StringVar()
        super(SettingDialog, self).__init__(parent, 'Setting', app)

    def body(self, frame):
        self.level_var.set(self.app.level.get())
        self.user_var.set(self.app.user.name)
        self.head_color = self.app.snake.color['head']
        self.body_color = self.app.snake.color['body']

        tk.Label(self, text='User:').place(x=20, y=20)
        tk.Entry(self, textvariable=self.user_var, width=17).place(x=60, y=22)

        tk.Label(self, text='Level:').place(x=20, y=60)
        tk.Scale(self, from_=1, to=3, variable=self.level_var, orient=tk.HORIZONTAL).place(x=65, y=42)

        tk.Label(self, text='Snake Head Color:').place(x=25, y=105)
        self.head_color_btn = tk.Button(self, bg=self.head_color, width=2, command=self.set_head_color)
        self.head_color_btn.place(x=135, y=105)

        tk.Label(self, text='Snake Body Color:').place(x=25, y=145)
        self.body_color_btn = tk.Button(self, bg=self.body_color, width=2, command=self.set_body_color)
        self.body_color_btn.place(x=135, y=145)

        tk.Button(self, text='Reset', width=10, command=self.reset).place(x=15, y=195)
        tk.Button(self, text='Apply', width=10, command=self.apply).place(x=105, y=195)

        self.geometry('200x240')
        self.resizable(False, False)
        self.bind('<Return>', lambda _: self.apply())
        self.bind('<Escape>', lambda _: self.reset())
        if is_windows:
            winsound.MessageBeep()

        return frame

    def set_head_color(self):
        self.head_color = colorchooser.askcolor(initialcolor=self.head_color)[1]
        self.head_color_btn.config(bg=self.head_color)

    def set_body_color(self):
        self.body_color = colorchooser.askcolor(initialcolor=self.body_color)[1]
        self.body_color_btn.config(bg=self.body_color)

    def apply(self):
        if self.level_var.get() != self.app.level.get() or self.user_var.get() != self.app.user.name:
            self.need_restart = True

        if self.need_restart and messagebox.askokcancel('Restart Game', 'Are you sure to restart the game?'):
            self.app.change_user(self.user_var.get())
            self.app.set_level(self.level_var.get())
            self.app.restart()

        self.app.snake.change_head_color(self.head_color)
        self.app.snake.change_body_color(self.body_color)
        self.app.user.snake_head_color = self.app.snake.color['head']
        self.app.user.snake_body_color = self.app.snake.color['body']
        self.app.user.save()

    def reset(self):
        self.head_color = self.app.snake.color['head']
        self.body_color = self.app.snake.color['body']
        self.head_color_btn.config(bg=self.head_color)
        self.body_color_btn.config(bg=self.body_color)
        self.level_var.set(self.app.level.get())
        self.user_var.set(self.app.user.name)


class AboutDialog(BaseDialog):
    def __init__(self, parent):
        super(AboutDialog, self).__init__(parent, 'About us')

    def body(self, frame):
        tk.Label(self, text='This game made by Sina.f & Mohammad Amini').pack(pady=12)
        grid_options = {'row': 1, 'padx': 15, 'pady': 15}

        sina_frame = tk.LabelFrame(self, text='Sina.f')
        sina_frame.pack(fill=tk.X, pady=5)
        tk.Button(sina_frame, text='GitHub', width=8,
                  command=lambda: webbrowser.open('https://github.com/sina-programer')).grid(column=1, **grid_options)
        tk.Button(sina_frame, text='Instagram', width=8,
                  command=lambda: webbrowser.open('https://www.instagram.com/sina.programer')).grid(column=2,
                                                                                                    **grid_options)
        tk.Button(sina_frame, text='Telegram', width=8,
                  command=lambda: webbrowser.open('https://t.me/sina_programer')).grid(column=3, **grid_options)

        mohammad_frame = tk.LabelFrame(self, text='Mohammad Amini')
        mohammad_frame.pack(fill=tk.X, pady=15)
        tk.Button(mohammad_frame, text='GitHub', width=8,
                  command=lambda: webbrowser.open('https://github.com/mohammadaminY')).grid(column=1, **grid_options)
        tk.Button(mohammad_frame, text='Instagram', width=8,
                  command=lambda: webbrowser.open('https://www.instagram.com/insta_id')).grid(column=2, **grid_options)
        tk.Button(mohammad_frame, text='Telegram', width=8,
                  command=lambda: webbrowser.open('https://t.me/tel_id')).grid(column=3, **grid_options)

        self.geometry('300x240')
        self.resizable(False, False)
        if is_windows:
            winsound.MessageBeep()

        return frame
