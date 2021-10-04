from base import PlayComponent
import random


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
