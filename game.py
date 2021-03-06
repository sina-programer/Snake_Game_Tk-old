import tkinter as tk
from time import sleep
from tkinter import messagebox
import sys
import random
from threading import Thread

import dialogs
# from bait import Bait
from ba import Ba
from snake import Snake
from database import User, Score
from relation import Relation


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
        self.is_online = False
        self.player_name = str(random.randint(10000 , 99999))
        self.relation = Relation(self.player_name)

        self.score.set(0)
        self.level.set(2)
        self.energy.set(200)
        self.change_user('Default')
        self.master.config(menu=self.init_menu())

        self.canvas = tk.Canvas(self, width=self.width, height=self.height)
        self.snake = Snake(self.canvas, (self.width / 2 - 20, self.height / 2), self.user.snake_head_color,
                           self.user.snake_body_color)

        self.bait = Ba(self.canvas, 'green')
        self.barrier = Ba(self.canvas, 'red', (25, 25))

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

    def check_collision(self, o1_pos, o1_size, o2_pos, o2_size):
        if (o1_pos[0] + (o1_size[0]/2) >= o2_pos[0] + (o2_size[0]/2) >= o1_pos[0] - (o1_size[0]/2) or \
            o1_pos[0] + (o1_size[0]/2) >= o2_pos[0] - (o2_size[0]/2) >= o1_pos[0] - (o1_size[0]/2)) \
            and \
            (o1_pos[1] + (o1_size[1]/2) >= o2_pos[1] + (o2_size[1]/2) >= o1_pos[1] - (o1_size[1]/2) or \
            o1_pos[1] + (o1_size[1]/2) >= o2_pos[1] - (o2_size[1]/2) >= o1_pos[1] - (o1_size[1]/2)):
            return True
        return False

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
        self.barrier.reset()

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


    def loss(self, message='You loss'):
        messagebox.showinfo('You loss', message)
        self.restart()

    def check_head_and_body_collision(self):
        if len(self.snake.body) > 1 and self.snake.check_collision_head_and_body():
            self.loss()

    def check_eating_bait(self):
        if self.check_collision(self.bait.get_position(), self.bait.size,
                            self.snake.get_position(self.snake.head),
                            self.snake.size):
        # if self.snake.get_position(self.snake.head) == self.bait.get_position():
            self.bait.move()
            self.energy.set(self.energy.get() + 30)
            self.score.set(self.score.get() + 1)
            self.snake.grow()

    def check_barrier_collision(self):
        if self.check_collision(self.barrier.get_position(), self.barrier.size,
                            self.snake.get_position(self.snake.head),
                            self.snake.size):
        # if self.snake.get_position(self.snake.head) == self.barrier.get_position():
            self.loss()

    def check_energy(self):
        energy = self.energy.get()
        if energy > 0:
            if self.snake.direction != 'stop':
                self.energy.set(energy - 1)
        else:
            self.loss('Your energies finished!')
            

    def set_level(self, level):
        self.level.set(level)
        self.delay = .15 - (self.level.get() / 100) * 2
        self.bait.set_level(self.level.get())
        self.barrier.set_level(self.level.get() * 3)

    def start_online(self):
        self.psnake = Snake(self.canvas, (self.width / 2 + 20, self.height / 2), 'red', 'red')
        self.is_online = True

    def play(self, player):
        status = self.relation.check_for_play()
        if status == 0:
            messagebox.showinfo("We can't play.")
        elif status == 2:
            messagebox.showinfo("Server don't send response.")
        elif status == 1:       
            Thread(target=self.start_online)

    def move_p(self):
        while True:
            pos = self.relation.get_pos()
            if not pos: break
            self.psnake.move(self.psnake, *pos)
            sleep(self.delay)
        messagebox.showinfo('end game', 'end game')

    def game_loop(self):
        while True:
            self.update()
            self.bait.check_auto_move()
            self.barrier.check_auto_move()
            self.check_eating_bait()
            self.check_barrier_collision()
            self.check_head_and_body_collision()
            self.snake.auto_move()
            if not self.is_online: self.check_energy()

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
        menu.add_command(label='Online', command=lambda: dialogs.OnlineDialog(self.master, self.play, self.player_name, self.relation))

        return menu


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    root.resizable(False, False)
    if 'win' in sys.platform:
        root.iconbitmap(default='Files/icon.ico')

    game = Game(root)
    game.mainloop()
