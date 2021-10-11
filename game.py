# import winsound
import webbrowser
import tkinter as tk
from time import sleep
from tkinter import simpledialog, messagebox, colorchooser

from bait import Bait
from snake import Snake
from database import User


class SettingDialog(simpledialog.Dialog):
    def __init__(self, parent, app):
        self.app = app
        self.level_var = tk.IntVar()
        self.level_var.set(self.app.level.get())
        self.color = {'head': 'black', 'body': 'grey'}
        super().__init__(parent, 'Setting')

    def body(self, frame):
        tk.Label(self, text='Level:').place(x=20, y=20)
        tk.Scale(self, from_=1, to=3, variable=self.level_var, orient=tk.HORIZONTAL).place(x=65, y=2)

        tk.Button(self, text='Apply', width=10, command=self.apply).place(x=80, y=130)

        tk.Button(self, text='Change snake head color', command=lambda: self.set_color()).place(x=1, y=55)
        tk.Button(self, text='Change snake body color', command=lambda: self.set_color(True)).place(x=1, y=90)

        self.geometry('200x180')
        self.resizable(False, False)
        self.bind('<Return>', lambda _: self.apply())
        # winsound.MessageBeep()

        return frame

    def set_color(self, for_body=False):
        if for_body:
            self.color['body'] = colorchooser.askcolor(master=self.master)[1]
        else:
            self.color['head'] = colorchooser.askcolor(master=self.master)[1]

    def apply(self):
        submit = messagebox.askokcancel('Restart Game', 'Are you sure to restart the game(reset scores)')
        if submit:
            self.app.change_snake_color(self.color['head'], self.color['body'])
            self.app.set_level(self.level_var.get())
            self.app.restart()

    def buttonbox(self):
        pass


class AboutDialog(simpledialog.Dialog):
    def __init__(self, parent):
        super().__init__(parent, 'About us')

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
        # winsound.MessageBeep()

        return frame

    def buttonbox(self):
        pass


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)

        self.best_score = tk.IntVar()

        try:
            self.user = User.select().where(User.name == 'Default').get()
            self.best_score.set(self.user.best_score)

        except:
            self.user = User(name='Default', best_score=0)
            self.best_score.set(0)

        self.user.save()
        self.username = self.user.name

        self.head_color = 'black'
        self.body_color = 'grey'
        self.font = ('arial', 20)
        self.score = tk.IntVar()
        self.score.set(0)
        self.width = 525
        self.height = 525
        self.energy = tk.IntVar()
        self.energy.set(420)
        self.delay = None
        self.level = tk.IntVar()
        self.master = master
        self.master.config(menu=self.init_menu())
        self.canvas = tk.Canvas(self, bg='lightblue', width=self.width, height=self.height)
        self.snake = Snake(self.canvas, self.width / 2, self.height / 2)
        self.bait = Bait(self.canvas)
        self.set_level(2)

        self.canvas.bind('<Left>', lambda _: self.snake.set_direction('left'))
        self.canvas.bind('<Right>', lambda _: self.snake.set_direction('right'))
        self.canvas.bind('<Up>', lambda _: self.snake.set_direction('up'))
        self.canvas.bind('<Down>', lambda _: self.snake.set_direction('down'))
        self.canvas.bind('<Escape>', lambda _: self.snake.set_direction('stop'))
        self.canvas.bind('<Enter>', lambda _: self.canvas.focus_force())
        self.canvas.focus_force()
        self.canvas.pack()
        self.pack(side=tk.BOTTOM, pady=5)

        tk.Label(self.master, text='Score:', font=self.font).pack(side=tk.LEFT, padx=5)
        tk.Label(self.master, textvariable=self.score, font=self.font).pack(side=tk.LEFT)

        tk.Label(self.master, text='Best Score:', font=self.font).place(x=160, y=10)
        tk.Label(self.master, textvariable=self.best_score, font=self.font).place(x=310, y=11)

        tk.Label(self.master, textvariable=self.energy, font=self.font).pack(side=tk.RIGHT, padx=8)
        tk.Label(self.master, text='Energy:', font=self.font).pack(side=tk.RIGHT)

        self.game_loop()

    def restart(self):
        score = self.score.get()

        if score > self.best_score.get():
            self.best_score.set(score)
            self.user.best_score = score
            self.user.save()

        self.energy.set(500 - self.level.get() * 40)
        self.score.set(0)
        self.snake.reset()
        self.bait.reset()

    def change_snake_color(self, head_color, body_color):
        self.snake.change_head_color(head_color)
        self.snake.change_body_color(body_color)

    def check_head_and_body_collision(self):
        if len(self.snake.body) > 1 and self.snake.check_collision_head_and_body():
            messagebox.showinfo('You loss', 'You loss')
            self.restart()

    def move_snake(self):
        self.snake.move_head()
        self.snake.delete_unuse_move_history(self.snake.history_of_move, len(self.snake.body))
        self.snake.save_move(self.snake.get_position(self.snake.snake_head))

    def check_eating_bait(self):
        if self.snake.get_position(self.snake.snake_head) == self.bait.get_position():
            self.bait.move()
            self.energy.set(self.energy.get() + 30)
            self.score.set(self.score.get() + 1)
            self.snake.add_body(len(self.snake.body))

    def check_energy(self):
        energy = self.energy.get()
        if energy > 0:
            if self.snake.direction != 'stop':
                self.energy.set(energy - 1)
        else:
            messagebox.showinfo('You loss', 'Your energies finished!')
            self.restart()

    def set_level(self, level):
        self.level.set(level)
        self.delay = .15 - (self.level.get() / 100) * 2
        self.bait.set_level(self.level.get())

    def init_menu(self):
        menu = tk.Menu(self.master)
        menu.add_command(label='Setting', command=lambda: SettingDialog(self.master, self))
        menu.add_command(label='About us', command=lambda: AboutDialog(self.master))

        return menu

    def game_loop(self):
        while True:
            self.update()
            self.bait.check_auto_move()
            self.check_eating_bait()
            self.check_head_and_body_collision()
            self.move_snake()
            self.check_energy()
            sleep(self.delay)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    # root.iconbitmap(default='Files/icon.ico')

    game = Game(root)
    game.mainloop()
