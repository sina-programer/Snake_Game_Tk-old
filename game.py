import pygame
from pygame import locals


class Game:
    def __init__(self):
        pygame.init()

        self.screen = pygame.display.set_mode((500, 400), 0, 32)
        self.clock = pygame.time.Clock()

        self.BLUE = (0, 0, 255)
        self.WHITE = (255, 255, 255)

        self.screen.fill(self.WHITE)
        self.snake = pygame.draw.rect(self.screen, self.BLUE, (20, 20, 20, 20))

    def drow(self):
        self.snake = pygame.draw.rect(self.screen, (0, 0, 128), self.snake)

    def start(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

            self.screen.fill((255, 255, 255))
            self.drow()
            self.key_handler()
            pygame.display.update()

            self.clock.tick(40)

    def key_handler(self):
        key = pygame.key.get_pressed()
        move = 5
        # and self.snake.top != self.screen.get_height() and self.snake.left != self.screen.get_width()

        if key[pygame.K_LEFT] and self.snake.left != 0:
            self.snake.move_ip(-move, 0)
        elif key[pygame.K_RIGHT] and self.snake.left != (self.screen.get_width() - self.snake.width):
            self.snake.move_ip(move, 0)
        elif key[pygame.K_UP] and self.snake.top != 0:
            self.snake.move_ip(0, -move)
        elif key[pygame.K_DOWN] and self.snake.top != (self.screen.get_height() - self.snake.height):
            self.snake.move_ip(0, move)
