class Snake:
    def __init__(self, canvas, x, y, head_color='black', body_color='grey'):
        self.canvas = canvas
        self.aims = {
            'stop': None,
            'up': (0, -15),
            'down': (0, 15),
            'left': (-15, 0),
            'right': (15, 0)
        }
        self.size = 15
        self.color = {'head': head_color, 'body': body_color}
        self.head = self.canvas.create_rectangle(x - self.size / 2,
                                                 y - self.size / 2,
                                                 x + self.size / 2,
                                                 y + self.size / 2,
                                                 fill=self.color['head'])
        self.body = []
        self.first_position = x, y
        self.last_aim = None
        self._direction = 'stop'
        self.history_of_move = [(x, y)]

    def reset(self):
        self.canvas.delete(self.head)
        self.head = self.canvas.create_rectangle(self.first_position[0] - self.size / 2,
                                                 self.first_position[1] - self.size / 2,
                                                 self.first_position[0] + self.size / 2,
                                                 self.first_position[1] + self.size / 2,
                                                 fill=self.color['head'])
        self.direction = 'stop'
        for body in self.body:
            self.canvas.delete(body)
        self.body = []

    @property
    def direction(self):
        return self._direction

    @direction.setter
    def direction(self, value):
        if value in self.aims.keys():
            self._direction = value
        else:
            raise ValueError(f'The direction must be in {list(self.aims.keys())} (your value : {value})')

    def change_body_color(self, color):
        self.color['body'] = color
        for body in self.body:
            self.canvas.itemconfig(body, fill=self.color['body'])

    def change_head_color(self, color):
        self.color['head'] = color
        self.canvas.itemconfig(self.head, fill=self.color['head'])

    def move_head(self):
        self.check_inside()
        aim = self.aims[self.direction]
        if aim is not None:
            if self.check_aim(self.aims, aim, self.last_aim):
                self.last_aim = aim
                self.move(*aim)
                self.move_body(self.body, self.history_of_move)
            else:
                self.move(*self.last_aim)
                self.move_body(self.body, self.history_of_move)

    @staticmethod
    def check_aim(aims, aim, last_aim):
        if aim == aims['up']:
            if last_aim != aims['down']:
                return True
        elif aim == aims['down']:
            if last_aim != aims['up']:
                return True
        elif aim == aims['right']:
            if last_aim != aims['left']:
                return True
        elif aim == aims['left']:
            if last_aim != aims['right']:
                return True
        return False

    def move(self, x, y):
        self.canvas.move(self.head, x, y)

    def move_body(self, body, snake_history_of_move):
        """
        This move the body of snake
        The snake_history_of_move must be tuple or list of coords
        :param body:
        :param snake_history_of_move:
        :return:
        """

        for i in range(len(body)):
            first_position = self.get_position(body[i])  # a body position
            next_position = self.get_next_position(snake_history_of_move, (first_position[0], first_position[1]), i)
            final_position = (next_position[0] - first_position[0], next_position[1] - first_position[1])
            self.canvas.move(body[i], final_position[0], final_position[1])

    @staticmethod
    def get_next_position(snake_history_of_move, position, body_index):
        index = 0
        found_head_position = False
        for p in reversed(snake_history_of_move):
            if found_head_position is not None:
                index += 1
                if body_index == (index - 1):
                    return p
            elif position == p:
                found_head_position = True
        return snake_history_of_move[-(body_index + 1)]

    def get_coords(self):
        return self.canvas.coords(self.head)

    def get_position(self, item):
        coords = self.canvas.coords(item)
        return (coords[2] - coords[0]) / 2 + coords[0], (coords[3] - coords[1]) / 2 + coords[1]

    def delete(self):
        self.canvas.delete(self.head)

    def save_move(self, position):
        if self.history_of_move[-1] != position:
            self.history_of_move.append(position)

    def check_collision_head_and_body(self):
        for body in self.body:
            if self.get_position(self.head) == self.get_position(body):
                return True
        return False

    @staticmethod
    def delete_unuse_move_history(history_of_move, body_number):
        history_of_move_copy = history_of_move.copy()
        history_of_move.clear()
        history_of_move.extend(history_of_move_copy[(-body_number - 1):])

    def add_body(self, body_number):
        x, y = self.history_of_move[-1]
        p = 8
        p = p * body_number
        self.body.append(self.canvas.create_rectangle(x - p,
                                                      y - p,
                                                      self.size + x - p,
                                                      self.size + y - p,
                                                      fill=self.color['body']))

    def set_direction(self, direction):
        if self.direction != direction:
            self.direction = direction

    def check_inside(self):
        coords = self.get_coords()

        if coords[0] <= 0 and self.direction == 'left':
            self.move(525, 0)
        elif coords[2] >= 525 and self.direction == 'right':
            self.move(-525, 0)

        if coords[1] <= 0 and self.direction == 'up':
            self.move(0, 525)
        elif coords[3] >= 525 and self.direction == 'down':
            self.move(0, -525)
