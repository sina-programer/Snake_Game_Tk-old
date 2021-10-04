from random import choice


class Snake:
    def __init__(self, canvas, x, y):
        self.aims = {
            'stop': None,
            'up': (0, -15),
            'down': (0, 15),
            'left': (-15, 0),
            'right': (15, 0)
        }
        self.last_aim = None
        self.direction = 'stop'
        self.size = 15
        snake_head = canvas.create_rectangle(x - self.size / 2,
                                             y - self.size / 2,
                                             x + self.size / 2,
                                             y + self.size / 2,
                                             fill='black')
        self.body = []
        self.history_of_move = [(x, y)]
        self.snake_head = snake_head
        self.canvas = canvas

    def move_head(self):
        self.check_inside()
        aim = self.aims[self.direction]
        if aim is not None:
            if self.check_aim(self.aims, aim, self.last_aim):
                self.last_aim = aim
                self.move(*aim)
                self.move_body(self.body, self.history_of_move, aim)
            else:
                self.move(*self.last_aim)
                self.move_body(self.body, self.history_of_move, self.last_aim)

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
            next_position = self.get_next_position(snake_history_of_move, (first_position[0], first_position[1]), i)
            final_position = (next_position[0] - first_position[0], next_position[1] - first_position[1])
            self.canvas.move(body[i], final_position[0], final_position[1])

    @staticmethod
    def get_next_position(snake_history_of_move, position, body_index):
        index = 0
        found_head_position = None
        for p in snake_history_of_move:
            if found_head_position:
                index += 1
                if found_head_position == index:
                    return p
            if position == p:
                found_head_position = body_index
        return snake_history_of_move[-body_index + 1]

    def get_coords(self):
        return self.canvas.coords(self.snake_head)

    def get_position(self, item):
        coords = self.canvas.coords(item)
        return (coords[2] - coords[0]) / 2 + coords[0], (coords[3] - coords[1]) / 2 + coords[1]

    def delete(self):
        self.canvas.delete(self.snake_head)

    def save_move(self, position):
        if self.history_of_move[-1] != position:
            self.history_of_move.append(position)

    @staticmethod
    def delete_unuse_move_history(history_of_move, body_number):
        history_of_move_copy = history_of_move.copy()
        history_of_move.clear()
        history_of_move.extend(history_of_move_copy[(-body_number - 1):])

    def add_body(self, body_number):
        x, y = self.history_of_move[-1]
        p = 8
        p = p * body_number
        colors = ('red', 'blue', 'green', 'yellow')
        random_color = choice(colors)
        print(random_color)
        self.body.append(
            self.canvas.create_rectangle(x - p, y - p, self.size + x - p, self.size + y - p, fill=random_color))

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
