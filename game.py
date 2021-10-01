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

        if key[pygame.K_LEFT]:
            self.snake.move_ip(0, 10)
