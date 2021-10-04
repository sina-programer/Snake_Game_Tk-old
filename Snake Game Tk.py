from threading import Thread
from time import sleep
from tkinter import *
import random


class PlayComponent:
    def __init__(self, canvas, snake_head):
        self.snake_head = snake_head
        self.canvas = canvas

    def move(self, x, y):
        self.canvas.move(self.snake_head, x, y)

    def move_body(self, body, snake_history_of_move, aim):
        """
        This move the body of snake
        The snake_history_of_move must be tuple or list of coords
        :param body:
        :param snake_history_of_move:
        :param aim:
        :return:
        """

        for i in range(len(body)):
            first_position = self.get_position(body[i])  # a body position
            next_position = self.get_next_position(snake_history_of_move, (first_position[0], first_position[1]))
            final_position = (next_position[0] - first_position[0], next_position[1] - first_position[1])
            self.canvas.move(body[i], *final_position)

    @staticmethod
    def get_next_position(snake_history_of_move, position):
        is_found = False
        for p in snake_history_of_move:
            if is_found:
                return p
            if position == p:
                is_found = True
        return snake_history_of_move[-1]

    def get_coords(self):
        return self.canvas.coords(self.snake_head)

    def get_position(self, item):
        coords = self.canvas.coords(item)
        return (coords[2] - coords[0]) / 2 + coords[0], (coords[3] - coords[1]) / 2 + coords[1]

    def delete(self):
        self.canvas.delete(self.snake_head)


class Bait(PlayComponent):
    def __init__(self, canvas):
        self.x = random.randrange(10, 520, 15) - 2.5
        self.y = random.randrange(10, 520, 15) - 2.5
        self.size = 15

        item = canvas.create_rectangle(self.x - self.size / 2,
                                       self.y - self.size / 2,
                                       self.x + self.size / 2,
                                       self.y + self.size / 2,
                                       fill='green')

        super(Bait, self).__init__(canvas, item)

    def move(self):
        self.x = random.randrange(10, 520, 15) - self.x - 2.5
        self.y = random.randrange(10, 520, 15) - self.y - 2.5
        super().move(self.x, self.y)


class Snake(PlayComponent):
    def __init__(self, canvas, x, y):
        self.aims = {
            'stop': None,
            'up': (0, -15),
            'down': (0, 15),
            'left': (-15, 0),
            'right': (15, 0)
        }
        self.direction = 'stop'
        self.size = 15
        snake_head = canvas.create_rectangle(x - self.size / 2,
                                             y - self.size / 2,
                                             x + self.size / 2,
                                             y + self.size / 2,
                                             fill='black')
        self.body = []
        self.history_of_move = [(x, y)]
        super(Snake, self).__init__(canvas, snake_head)

    def move(self):
        self.check_inside()
        aim = self.aims.get(self.direction)
        if aim is not None:
            super().move(*aim)
            super().move_body(self.body, self.history_of_move, aim)

    def save_move(self, position):
        if self.history_of_move[-1] != position:
            self.history_of_move.append(position)

    def delete_unuse_move_history(self, history_of_move, body_number):
        history_of_move_copy = history_of_move.copy()
        history_of_move.clear()
        history_of_move.extend(history_of_move_copy[-body_number:])

    def add_body(self,body_number):
        x, y = self.history_of_move[-1]
        p = 8
        p=p * body_number
        self.body.append(self.canvas.create_rectangle(x - p, y - p, self.size + x - p, self.size + y - p, fill='red'))

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction

    def check_inside(self):
        coords = self.get_coords()

        if coords[0] <= 0 and self.direction == 'left':
            super().move(525, 0)
        elif coords[2] >= 525 and self.direction == 'right':
            super().move(-525, 0)

        if coords[1] <= 0 and self.direction == 'up':
            super().move(0, 525)
        elif coords[3] >= 525 and self.direction == 'down':
            super().move(0, -525)


class Game(Frame):
    def __init__(self, master):
        super(Game, self).__init__(master)

        self.score = IntVar()
        self.score.set(0)
        self.width = 525
        self.height = 525
        self.canvas = Canvas(self, bg='lightblue', width=self.width, height=self.height)
        self.canvas.pack()

        self.pack(side=BOTTOM, pady=5)
        Label(master, text='Score:', font=('arial', 20)).pack(side=LEFT, padx=5)
        Label(master, textvariable=self.score, font=('arial', 20)).pack(side=LEFT)

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
            if self.snake.get_position(self.snake.snake_head) == self.bait.get_position(self.bait.snake_head):
                self.bait.move()
                self.score.set(self.score.get() + 1)
                self.snake.add_body(len(self.snake.body))
                print('length', len(self.snake.body))
                print(self.snake.get_position(self.snake.body[0]))

            self.snake.move()
            self.snake.delete_unuse_move_history(self.snake.history_of_move, len(self.snake.body))
            self.snake.save_move(self.snake.get_position(self.snake.snake_head))
            sleep(.15)


if __name__ == "__main__":
    root = Tk()
    root.title('Snake Game')
    root.geometry('540x600+440+130')
    # root.iconbitmap('Files/icon.ico')

    game = Game(root)
    game.mainloop()
