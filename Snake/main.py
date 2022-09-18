import pygame
from pygame.locals import *
import time
import random

SIZE = 50
LENGTH = 2
WHITE = (255, 255, 255)
BACKGROUND = (43, 232, 30)
BACKGROUND2 = (82, 240, 46)


class Java:
    def __init__(self, surface):
        self.surface = surface
        self.food = pygame.image.load("Resources/java.jpeg").convert()
        self.x = 450
        self.y = 350

    def draw(self):
        self.surface.blit(self.food, (self.x, self.y))
        pygame.display.flip()

    def eaten(self):
        self.x = random.randint(0, 14) * SIZE
        self.y = random.randint(0, 14) * SIZE
        self.draw()


class Snake:
    def __init__(self, surface, length):
        self.surface = surface
        self.length = length
        self.head = pygame.image.load("Resources/head1_right.jpeg").convert()
        self.body = pygame.image.load("Resources/body1.jpeg").convert()
        self.x = [200] * length
        self.y = [350] * length
        self.direction = "right"
        self.python = 1

    def lose(self):
        if self.x[0] < 0 or self.y[0] < 0 or self.x[0] >= 750 or self.y[0] >= 750:
            return True
        for i in range(1, self.length):
            if self.x[0] == self.x[i] and self.y[0] == self.y[i]:
                return True
        return False

    def grow(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

    def draw(self):
        self.head = pygame.image.load(f"Resources/head{self.python}_{self.direction}.jpeg").convert()
        self.body = pygame.image.load(f"Resources/body{self.python}.jpeg").convert()
        self.surface.blit(self.head, (self.x[0], self.y[0]))
        for i in range(self.length - 1):
            self.surface.blit(self.body, (self.x[i + 1], self.y[i + 1]))
        pygame.display.flip()

    def move(self):
        for i in range(self.length - 1):
            self.x[self.length - i - 1] = self.x[self.length - i - 2]
            self.y[self.length - i - 1] = self.y[self.length - i - 2]

        if self.direction == "right":
            self.x[0] += SIZE
        if self.direction == "left":
            self.x[0] -= SIZE
        if self.direction == "up":
            self.y[0] -= SIZE
        if self.direction == "down":
            self.y[0] += SIZE
        self.draw()

    def switch(self):
        last = self.length - 1
        if self.x[last] > self.x[last - 1]:
            self.direction = "right"
        elif self.x[last] < self.x[last - 1]:
            self.direction = "left"
        elif self.y[last] > self.y[last - 1]:
            self.direction = "down"
        elif self.y[last] < self.y[last - 1]:
            self.direction = "up"

        if self.python == 1:
            self.python = 2
        else:
            self.python = 1

        self.x.reverse()
        self.y.reverse()


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Python Snake")
        pygame.mixer.init()
        self.surface = pygame.display.set_mode((750, 750))
        self.surface.fill(BACKGROUND)
        self.music()
        self.checkered()
        self.snake = Snake(self.surface, LENGTH)
        self.snake.draw()
        self.java = Java(self.surface)
        self.java.draw()
        self.high_score = 0
        self.original_high = 0

    def score(self):
        pygame.draw.rect(self.surface, BACKGROUND2, (8 * SIZE, 0, SIZE, SIZE))
        font = pygame.font.SysFont('arial', 34)
        length = self.snake.length - LENGTH
        score = font.render(f"Javas: {length}", True, WHITE)
        self.surface.blit(score, (300, 15))
        if length > self.high_score:
            self.high_score = length
            pygame.draw.rect(self.surface, BACKGROUND, (13 * SIZE, 0, SIZE, SIZE))
        high = font.render(f"High Score: {self.high_score}", True, WHITE)
        self.surface.blit(high, (465, 15))
        pygame.display.flip()

    def sound_effect(self, sound_name):
        sound = pygame.mixer.Sound(f"Resources/{sound_name}")
        pygame.mixer.Sound.play(sound)

    def music(self):
        pygame.mixer.music.load("Resources/Lofi.mp3")
        pygame.mixer.music.play(-1)

    def cover_path(self):
        last = self.snake.length - 1
        lastx = self.snake.x[last]
        lasty = self.snake.y[last]
        if (lastx % 100 == 0 and lasty % 100 == 0) or (lastx % 100 != 0 and lasty % 100 != 0):
            color = BACKGROUND2
        else:
            color = BACKGROUND
        pygame.draw.rect(self.surface, color, (lastx, lasty, SIZE, SIZE))

    def play(self):
        self.cover_path()
        self.snake.move()
        self.java.draw()
        self.score()

        if self.snake.x[0] == self.java.x and self.snake.y[0] == self.java.y:
            self.sound_effect("Drink.wav")
            self.java.eaten()
            self.snake.grow()

        if self.snake.lose():
            self.sound_effect("Death.mp3")
            raise "Game Over!"

    def checkered(self):
        for row in range(15):
            for col in range(row % 2, 15, 2):
                pygame.draw.rect(self.surface, BACKGROUND2, (row * SIZE, col * SIZE, SIZE, SIZE))

    def sorry(self):
        self.surface.fill(BACKGROUND)
        font0 = pygame.font.SysFont('arial', 80)
        font = pygame.font.SysFont('arial', 35)
        if self.original_high < self.high_score:
            line = font0.render("New High Score!", True, WHITE)
            self.surface.blit(line, (82, 270))
            enter = 430
        else:
            line = font0.render("Game Over!", True, WHITE)
            self.surface.blit(line, (160, 270))
            enter = 480
            line3 = font.render(f"Want to beat your high score of {self.high_score}?", True, WHITE)
            self.surface.blit(line3, (105, 430))

        line1 = font.render(f"Score: {self.snake.length - LENGTH} Javas", True, WHITE)
        self.surface.blit(line1, (263, 380))
        line2 = font.render("Click Enter to Play Again!", True, WHITE)
        self.surface.blit(line2, (190, enter))
        pygame.display.flip()

    def reset(self):
        self.surface.fill(BACKGROUND)
        self.checkered()
        self.snake = Snake(self.surface, LENGTH)
        self.java = Java(self.surface)
        self.original_high = self.high_score

    def run(self):
        running = True
        stop = False
        while running:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    if event.key == K_RETURN:
                        stop = False
                    if not stop:
                        if event.key == K_SPACE:
                            if not self.snake.x[self.snake.length - 1] < 0:
                                self.snake.switch()
                        if event.key == K_LEFT and self.snake.direction != "right":
                            self.snake.direction = "left"
                        if event.key == K_RIGHT and self.snake.direction != "left":
                            self.snake.direction = "right"
                        if event.key == K_UP and self.snake.direction != "down":
                            self.snake.direction = "up"
                        if event.key == K_DOWN and self.snake.direction != "up":
                            self.snake.direction = "down"
                elif event.type == QUIT:
                    running = False

            try:
                if not stop:
                    self.play()
            except Exception as e:
                self.sorry()
                stop = True
                self.reset()
            time.sleep(0.1)


if __name__ == "__main__":
    game = Game()
    game.run()

