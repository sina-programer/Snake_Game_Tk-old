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
