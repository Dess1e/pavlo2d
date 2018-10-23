
from random import randrange
import schedule
import pdb
from Objects import *

pygame.init()
global_vars = {
    'WIDTH': 640,
    'HEIGHT': 480,
    'BG_COLOR': (0, 0, 0),
}
WIDTH, HEIGHT = global_vars['WIDTH'], global_vars['HEIGHT']
screen = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
CLOCK.tick()


def check_events(keymap):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key in keymap:
                keymap[event.key]()


def populate(grp):
    coord = randrange(0, WIDTH)
    b = Block('pavlo32.png', (coord, 0))
    grp.add(b)


def main():
    player = PhysicsPlayer('star32.png', (WIDTH // 2 - 32, HEIGHT - 32))
    actors = [
        player,
    ]
    keymap = {
        276: lambda: player.move_left(),
        275: lambda: player.move_right(),
    }
    grp = pygame.sprite.Group()
    schedule.every(0.25).seconds.do(lambda: populate(grp))

    while True:
        check_events(keymap)
        schedule.run_pending()
        if player.check_collision(grp):
            sys.exit()
        screen.fill(global_vars['BG_COLOR'])

        delta_t = CLOCK.tick(120) * 10 ** -3
        for actor in actors + list(grp):
            actor.tick(delta_t)
            actor.render(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
