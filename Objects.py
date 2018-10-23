import pygame
import sys
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
        self.rect = self.rect.move_ip(x, y)

    def get_rect(self):
        return self.img.get_rect()

    def render(self, screen):
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

    # def check_collision(self, group, dokill=False, collided=None):
    #     col = pygame.sprite.spritecollide(self, group, dokill, collided)
    #     if col:
    #         sys.exit()


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
    def __init__(self, *args):
        super().__init__(*args)

    def tick(self, delta_time):
        delta_y = delta_time * 250
        self.move(0, delta_y)
        if self.rect.y > global_vars['HEIGHT']:
            self.kill()


class FullscreenText(pygame.font.Font):
    def __init__(self, *args):
        super().__init__(*args)
        self.surface = self.render('TU PROEBAV', True, (255,255,255))

    def draw(self, screen):
        screen.blit(self.surface, self.get_rect())


