import tkinter as tk
from time import sleep
from tkinter import messagebox

import dialogs
from bait import Bait
from snake import Snake
from database import User


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)

        self.best_score = tk.IntVar()

        try:
            self.user = User.select().where(User.name == 'Default').get()
            self.best_score.set(self.user.best_score)
        except:
            self.user = User(name='Default', best_score=0, head_color='black', body_color='grey')
            self.best_score.set(0)

        self.user.save()
        self.username = self.user.name

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

        self.snake = Snake(self.canvas, self.width / 2, self.height / 2, self.user.head_color, self.user.body_color)
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

    def check_head_and_body_collision(self):
        if len(self.snake.body) > 1 and self.snake.check_collision_head_and_body():
            messagebox.showinfo('You loss', 'You loss')
            self.restart()

    def move_snake(self):
        self.snake.move_head()
        self.snake.delete_unuse_move_history(self.snake.history_of_move, len(self.snake.body))
        self.snake.save_move(self.snake.get_position(self.snake.head))

    def check_eating_bait(self):
        if self.snake.get_position(self.snake.head) == self.bait.get_position():
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

    def game_loop(self):
        while True:
            self.update()
            self.bait.check_auto_move()
            self.check_eating_bait()
            self.check_head_and_body_collision()
            self.move_snake()
            self.check_energy()
            sleep(self.delay)

    def init_menu(self):
        menu = tk.Menu(self.master)
        menu.add_command(label='Best scores', command=lambda: dialogs.BestScoresDialog(self.master, self))
        menu.add_command(label='Setting', command=lambda: dialogs.SettingDialog(self.master, self))
        menu.add_command(label='About us', command=lambda: dialogs.AboutDialog(self.master))

        return menu


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    root.iconbitmap(default='Files/icon.ico')

    game = Game(root)
    game.mainloop()
