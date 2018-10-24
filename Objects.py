import pygame
import sys
from random import randrange
from math import sqrt
from main import global_vars


class Actor(pygame.sprite.Sprite):
    def __init__(self, resource, coords):
        pygame.sprite.Sprite.__init__(self)
        self.img = pygame.image.load(resource)
        self.coords = list(coords)
        self.rect = self.img.get_rect()
        self.rect.move_ip(coords)

    def move(self, dx, dy):
        self.coords[0] += dx
        self.coords[1] += dy
        self.rect = self.rect.move(dx, dy)

    def set_coords(self, x, y):
        self.coords[0] = x
        self.coords[1] = y
        self.rect.x, self.rect.y = x, y

    def get_rect(self):
        return self.img.get_rect()

    def draw(self, screen):
        screen.blit(self.img, self.rect)

    def check_collision(self, group, dokill=False, collided=None):
        return pygame.sprite.spritecollide(self, group, dokill, collided)


class Player(Actor):
    def __init__(self, *args):
        super().__init__(*args)

    def move_left(self, delta):
        if self.rect.x < 0:
            return
        self.move(-delta, 0)

    def move_right(self, delta):
        if self.rect.x > global_vars['WIDTH'] - 32:
            return
        self.move(+delta, 0)


class PhysicsPlayer(Player):
    SPEED = 700

    def __init__(self, *args):
        super().__init__(*args)
        self.velocity = 0

    def move_left(self, v=0):
        self.velocity -= self.SPEED

    def move_right(self, v=0):
        self.velocity += self.SPEED

    def tick(self, delta_time):
        delta_move = abs(self.velocity) * delta_time
        if self.velocity > 0:
            super().move_right(delta_move)
            self.velocity = self.velocity - sqrt(self.velocity)
        elif self.velocity < 0:
            super().move_left(delta_move)
            self.velocity = self.velocity + sqrt(abs(self.velocity))


class Block(Actor):
    SPEED = 250
    SPEED_DIFF_COEF = 5

    def __init__(self, *args):
        super().__init__(*args)
        self.speed = self.SPEED + randrange(-self.SPEED // self.SPEED_DIFF_COEF,
                                            self.SPEED // self.SPEED_DIFF_COEF)

    def tick(self, delta_time):
        delta_y = delta_time * self.speed
        self.move(0, delta_y)
        if self.rect.y > global_vars['HEIGHT']:
            self.kill()


class Text:
    def __init__(self, size, color=(255, 255, 255), name=None, pos=(0, 0), text=''):
        if not name:
            self.name = pygame.font.get_default_font()
        else:
            self.name = name
        self.size = size
        self.pos = pos
        self.color = color
        self.font = pygame.font.SysFont(name, size)
        self.surface = self.font.render(text, True, color)

    def render_surface(self, text):
        self.surface = self.font.render(text, True, self.color)

    def draw(self, screen):
        screen.blit(self.surface, self.pos)

    def tick(self, delta):
        ...


class GameOverText(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.render_surface('TU PROEBAV')


class ScoreText(Text):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.score = 0

    def tick(self, delta):
        self.render_surface('Score: {}'.format(self.score))
