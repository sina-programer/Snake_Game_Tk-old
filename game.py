import tkinter as tk
from time import sleep
from tkinter import messagebox
import platform

import dialogs
from bait import Bait
from snake import Snake
from database import User, Score


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)

        self.font = ('arial', 20)
        self.best_score = tk.IntVar()
        self.energy = tk.IntVar()
        self.level = tk.IntVar()
        self.score = tk.IntVar()
        self.master = master
        self.canvas = None
        self.height = 525
        self.width = 525
        self.delay = None
        self.user = None

        self.score.set(0)
        self.level.set(2)
        self.energy.set(200)
        self.change_user('Default')
        self.master.config(menu=self.init_menu())

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.snake = Snake(self.canvas, self.width / 2, self.height / 2, self.user.snake_head_color,
                           self.user.snake_body_color)
        self.bait = Bait(self.canvas)
        self.update_personalizations()
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
        if score:
            Score(user=self.user, score=score, level=self.level.get(), best_score=self.best_score.get()).save()

        self.energy.set(300 - self.level.get() * 50)
        self.score.set(0)
        self.snake.reset()
        self.bait.reset()

    def change_user(self, username):
        try:
            self.user = User.get(username=username)
        except:
            self.user = User.create(username=username, password='', snake_head_color='black', snake_body_color='grey',
                                    background_color='#ADD8E6')
            self.user.save()

        self.update_best_score()
        if self.canvas:
            self.update_personalizations()

    def update_personalizations(self):
        self.canvas.config(bg=self.user.background_color)
        self.snake.change_head_color(self.user.snake_head_color)
        self.snake.change_body_color(self.user.snake_body_color)

    def update_best_score(self):
        try:
            score = Score.select().where(Score.user == self.user, Score.level == self.level.get()).order_by(
                Score.score.desc()).get()
            self.best_score.set(score.score)
        except:
            self.best_score.set(0)

    def check_head_and_body_collision(self):
        if len(self.snake.body) > 1 and self.snake.check_collision_head_and_body():
            messagebox.showinfo('You loss', 'You loss')
            self.restart()

    def check_eating_bait(self):
        if self.snake.get_position(self.snake.head) == self.bait.get_position():
            self.bait.move()
            self.energy.set(self.energy.get() + 30)
            self.score.set(self.score.get() + 1)
            self.snake.grow()

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

    def game_loop(self):
        while True:
            self.update()
            self.bait.check_auto_move()
            self.check_eating_bait()
            self.check_head_and_body_collision()
            self.snake.auto_move()
            self.check_energy()
            sleep(self.delay)

    def init_menu(self):
        menu = tk.Menu(self.master)

        account_menu = tk.Menu(menu, tearoff=False)
        account_menu.add_command(label='Sign in', command=lambda: dialogs.SigninDialog(self.master, self))
        account_menu.add_command(label='Sign up', command=lambda: dialogs.SignupDialog(self.master, self))
        account_menu.add_command(label='Manage Account', command=lambda: dialogs.ManageAccountDialog(self.master, self))

        menu.add_cascade(label='Account setting', menu=account_menu)
        menu.add_command(label='Best scores', command=lambda: dialogs.BestScoresDialog(self.master, self))
        menu.add_command(label='Setting', command=lambda: dialogs.SettingDialog(self.master, self))
        menu.add_command(label='About us', command=lambda: dialogs.AboutDialog(self.master))

        return menu


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    root.resizable(False, False)
    if 'windows' in platform.platform():
        root.iconbitmap(default='Files/icon.ico')

    game = Game(root)
    game.mainloop()
