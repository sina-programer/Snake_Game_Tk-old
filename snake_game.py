from time import sleep
from threading import Thread
import tkinter as tk
from snake import Snake
from bait import Bait


class Game(tk.Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)

        self.score = tk.IntVar()
        self.score.set(0)
        self.width = 525
        self.height = 525
        self.canvas = tk.Canvas(self, bg='lightblue', width=self.width, height=self.height)
        self.canvas.pack()

        self.pack(side=tk.BOTTOM, pady=5)
        tk.Label(master, text='Score:', font=('arial', 20)).pack(side=tk.LEFT, padx=5)
        tk.Label(master, textvariable=self.score, font=('arial', 20)).pack(side=tk.LEFT)

        self.snake = Snake(self.canvas, self.width / 2, self.height / 2)
        self.bait = Bait(self.canvas)

        self.canvas.focus_force()
        self.canvas.bind('<Left>', lambda _: self.snake.set_direction('left'))
        self.canvas.bind('<Right>', lambda _: self.snake.set_direction('right'))
        self.canvas.bind('<Up>', lambda _: self.snake.set_direction('up'))
        self.canvas.bind('<Down>', lambda _: self.snake.set_direction('down'))
        self.canvas.bind('<Escape>', lambda _: self.snake.set_direction('stop'))

        Thread(target=self.game_loop).start()

    def game_loop(self):
        while True:
            if self.snake.get_position(self.snake.snake_head) == self.bait.get_position():
                self.bait.move()
                self.score.set(self.score.get() + 1)
                self.snake.add_body(len(self.snake.body))
                print('length', len(self.snake.body))
                if len(self.snake.body) >= 2:
                    print(self.snake.get_position(self.snake.body[0]), self.snake.get_position(self.snake.body[1]))

            self.snake.move_head()
            self.snake.delete_unuse_move_history(self.snake.history_of_move, len(self.snake.body))
            self.snake.save_move(self.snake.get_position(self.snake.snake_head))
            sleep(.15)


if __name__ == "__main__":
    root = tk.Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    # root.iconbitmap('Files/icon.ico')

    game = Game(root)
    game.mainloop()
