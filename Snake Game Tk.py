from tkinter import *
from time import sleep
from threading import Thread

class PlayComponent:
    def __init__(self, canvas, item):
        self.item = item
        self.canvas = canvas
        
    def move(self, x, y):
        self.canvas.move(self.item, x, y)
        
    def position(self):
        return self.canvas.coords(self.item)
    
    def delete(self):
        self.canvas.delete(self.item)
        

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
        self.segments = []
        self.size = 15
        item = canvas.create_rectangle(x-self.size/2,
                                       y-self.size/2,
                                       x+self.size/2,
                                       y+self.size/2,
                                       fill='black')
        
        super(Snake, self).__init__(canvas, item)
        
    def move(self):
        self.check_inside()
        aim = self.aims.get(self.direction)
        if aim is not None:
            super().move(*aim)
    
    def set_direction(self, direction):
        self.direction = direction
    
    def check_inside(self):
        coords = self.position()

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
        
        self.score = 0
        self.width = 525
        self.height = 525
        self.canvas = Canvas(self, bg='lightblue', width=self.width, height=self.height)
        self.canvas.pack()
        self.pack(pady=5)
        
        self.snake = Snake(self.canvas, self.width/2, self.height/2)
        
        self.canvas.focus_set()
        self.canvas.bind('<Left>', lambda _: self.snake.set_direction('left'))
        self.canvas.bind('<Right>', lambda _: self.snake.set_direction('right'))
        self.canvas.bind('<Up>', lambda _: self.snake.set_direction('up'))
        self.canvas.bind('<Down>', lambda _: self.snake.set_direction('down'))
        self.canvas.bind('<Escape>', lambda _: self.snake.set_direction('stop'))
                
        main_thread = Thread(target=self.game_loop)
        main_thread.start()

    def game_loop(self):
        while True:
            self.snake.move()
            sleep(.15)
    

if __name__ == "__main__":
    root = Tk()
    root.title('Snake Game')
    root.geometry('540x540+440+130')
    root.iconbitmap('Files/icon.ico')
    
    game = Game(root)
    game.mainloop()
    
