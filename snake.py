class Snake:
    def __init__(self, canvas, x, y, head_color='black', body_color='grey'):
        self.size = (15, 15)
        self.body = []
        self.canvas = canvas
        self._direction = 'stop'
        self.start_position = x, y
        self.color = {'head': head_color, 'body': body_color}
        self.aims = {
            'stop': None,
            'up': (0, -15),
            'down': (0, 15),
            'left': (-15, 0),
            'right': (15, 0)
        }
        self.head = self.canvas.create_rectangle(x - self.size[0] / 2,
                                                 y - self.size[1] / 2,
                                                 x + self.size[0] / 2,
                                                 y + self.size[1] / 2,
                                                 fill=self.color['head'])

    def auto_move(self):
        self.check_inside()
        aim = self.aims[self.direction]
        if aim is not None:
            last_pos = self.get_position(self.head)
            self.canvas.move(self.head, *aim)

            for body in self.body:
                temp_pos = self.get_position(body)
                self.move(body, *last_pos)
                last_pos = temp_pos

    def grow(self):
        x, y = self.get_position(self.head)
        aim = self.aims[self.direction]
        x -= aim[0]
        y -= aim[1]
        self.body.append(self.canvas.create_rectangle(x - self.size[0] / 2,
                                                      y - self.size[1] / 2,
                                                      x + self.size[0] / 2,
                                                      y + self.size[1] / 2,
                                                      fill=self.color['body']))

    def reset(self):
        self.canvas.delete(self.head)
        self.head = self.canvas.create_rectangle(self.start_position[0] - self.size[0] / 2,
                                                 self.start_position[1] - self.size[1] / 2,
                                                 self.start_position[0] + self.size[0] / 2,
                                                 self.start_position[1] + self.size[1] / 2,
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
            if self.direction == 'stop' or value == 'stop':
                self._direction = value
            else:
                modes = list(self.aims.keys())[1:]
                idx = modes.index(value) // 2
                idx += 1 if idx else idx
                if self.direction not in modes[idx:idx + 2]:
                    self._direction = value

        else:
            raise ValueError(f'The direction must be in {list(self.aims.keys())} (your value : {value})')

    def check_inside(self):
        coords = self.canvas.coords(self.head)

        if coords[0] <= 0 and self.direction == 'left':
            self.canvas.move(self.head, 525, 0)
        elif coords[2] >= 525 and self.direction == 'right':
            self.canvas.move(self.head, -525, 0)

        if coords[1] <= 0 and self.direction == 'up':
            self.canvas.move(self.head, 0, 525)
        elif coords[3] >= 525 and self.direction == 'down':
            self.canvas.move(self.head, 0, -525)

    def check_collision_head_and_body(self):
        for body in self.body:
            if self.get_position(self.head) == self.get_position(body):
                return True
        return False

    def change_body_color(self, color):
        self.color['body'] = color
        for body in self.body:
            self.canvas.itemconfig(body, fill=self.color['body'])

    def change_head_color(self, color):
        self.color['head'] = color
        self.canvas.itemconfig(self.head, fill=self.color['head'])

    def get_position(self, item):
        coords = self.canvas.coords(item)
        return (coords[2] - coords[0]) / 2 + coords[0], (coords[3] - coords[1]) / 2 + coords[1]

    def move(self, item, x, y):
        item_pos = self.get_position(item)
        self.canvas.move(item, -item_pos[0], -item_pos[1])
        self.canvas.move(item, x, y)

    def set_direction(self, aim):
        self.direction = aim
