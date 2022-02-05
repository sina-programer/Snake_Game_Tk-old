# import random
# from creator import Creator


# class Bait(Creator):
#     def __init__(self, canvas):
#         self.x = random.randrange(10, 520, 15) - 2.5
#         self.y = random.randrange(10, 520, 15) - 2.5
#         self.canvas = canvas
#         self.time_to_move = None
#         self.timer = None
#         self.size = 15
#         self.item = canvas.create_rectangle(self.x - self.size / 2,
#                                             self.y - self.size / 2,
#                                             self.x + self.size / 2,
#                                             self.y + self.size / 2,
#                                             fill='green')

#     def move(self):
#         self.timer = self.time_to_move
#         self.canvas.move(self.item, -self.x, -self.y)
#         self.x = random.randrange(10, 520, 15) - 2.5
#         self.y = random.randrange(10, 520, 15) - 2.5
#         self.canvas.move(self.item, self.x, self.y)

#     def reset(self):
#         self.timer = self.time_to_move

#     def get_position(self):
#         coords = self.canvas.coords(self.item)
#         return (coords[2] - coords[0]) / 2 + coords[0], (coords[3] - coords[1]) / 2 + coords[1]

#     def set_level(self, level):
#         self.time_to_move = 100 - level * 8
#         self.timer = self.time_to_move

#     def check_auto_move(self):
#         if self.timer > 0:
#             self.timer -= 1
#         else:
#             self.move()
