import tkinter as tk
from tkinter import simpledialog, messagebox
from database import Database
from threading import Thread
from snake import Snake
from time import sleep
from bait import Bait


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)
        
        self.database = Database()

        
        self.font = ('arial', 20)
        self.score = tk.IntVar()
        self.score.set(0)
        self.width = 525
        self.height = 525
        self.level = None
        self.master = master
        self.canvas = tk.Canvas(self, bg='lightblue', width=self.width, height=self.height)
        self.canvas.pack()
        self.canvas.focus_force()
        self.pack(side=tk.BOTTOM, pady=5)
        
        tk.Label(self.master, text='Score:', font=self.font).pack(side=tk.LEFT, padx=5)
        tk.Label(self.master, textvariable=self.score, font=self.font).pack(side=tk.LEFT)

        self.level = simpledialog.askinteger('Level', 'Select a level:(3 hardest)', minvalue=1, maxvalue=3)
        while self.level is None:
            self.level = simpledialog.askinteger('Level', 'Select a level:(3 hardest)', minvalue=1, maxvalue=3)
        tk.Label(self.master, text=self.level, font=self.font).pack(side=tk.RIGHT, padx=8)
        tk.Label(self.master, text='Level:', font=self.font).pack(side=tk.RIGHT)

        self.snake = Snake(self.canvas, self.width/2, self.height/2)
        self.bait = Bait(self.canvas, self.level)

        self.canvas.bind('<Left>', lambda _: self.snake.set_direction('left'))
        self.canvas.bind('<Right>', lambda _: self.snake.set_direction('right'))
        self.canvas.bind('<Up>', lambda _: self.snake.set_direction('up'))
        self.canvas.bind('<Down>', lambda _: self.snake.set_direction('down'))
        self.canvas.bind('<Escape>', lambda _: self.snake.set_direction('stop'))

        Thread(target=self.game_loop).start()

    def restart(self):
        self.score.set(0)
        self.snake.reset()
        self.bait.reset()

    def game_loop(self):
        delay = .15 - (self.level/100) * 2
        while True:
            if self.snake.get_position(self.snake.snake_head) == self.bait.get_position():
                self.bait.move()
                self.score.set(self.score.get() + 1)
                self.snake.add_body(len(self.snake.body))

            self.snake.move_head()
            self.snake.delete_unuse_move_history(self.snake.history_of_move, len(self.snake.body))
            self.snake.save_move(self.snake.get_position(self.snake.snake_head))
            if len(self.snake.body) > 1 and self.snake.check_collision_head_and_body():
                messagebox.showinfo('You loss', 'You loss')
                self.restart()

            sleep(delay)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    # root.iconbitmap(default='Files/icon.ico')

    game = Game(root)
    game.mainloop()
