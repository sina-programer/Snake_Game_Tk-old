from base import PlayComponent


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

    def add_body(self, body_number):
        x, y = self.history_of_move[-1]
        p = 8
        p = p * body_number
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
