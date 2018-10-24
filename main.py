
from random import randrange
import schedule
import pdb
from Objects import *

pygame.init()
pygame.font.init()
global_vars = {
    'WIDTH': 1024,
    'HEIGHT': 768,
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
            print(event.key)
            if event.key in keymap:
                keymap[event.key]()


def populate(grp):
    coord = randrange(0, WIDTH)
    pavlo_selector = randrange(1, 5)
    b = Block(f'pavlo{pavlo_selector}.png', (coord, 0))
    grp.add(b)


def main():
    player = PhysicsPlayer('star32.png', (WIDTH // 2 - 32, HEIGHT - 32))
    score_text = ScoreText(30)
    actors = [
        player,
        score_text,
    ]
    keymap = {
        276: lambda: player.move_left(),
        275: lambda: player.move_right(),
        114: lambda: reset(),
        27: lambda: do_exit(),
    }
    grp = pygame.sprite.Group()
    schedule.every(0.25).seconds.do(lambda: populate(grp))

    def do_exit():
        t = Text(70, text='TU DOVBAEB', pos=(100, 100))
        t.draw(screen)
        pygame.display.flip()
        pygame.time.wait(2000)
        exit(0)

    def reset():
        grp.empty()
        player.set_coords(WIDTH // 2 - 32, HEIGHT - 32)
        player.velocity = 0
        score_text.score = 0

    while True:
        if player.check_collision(grp):
            f = Text(70, text='TU PROEBAV NAHUI', pos=(100, 100))
            f.draw(screen)
            pygame.display.flip()
            pygame.time.wait(2000)
            reset()

        check_events(keymap)
        schedule.run_pending()

        Block.SPEED += 10 ** -2
        score_text.score += 1

        screen.fill(global_vars['BG_COLOR'])
        delta_t = CLOCK.tick(120) * 10 ** -3
        for actor in actors + list(grp):
            actor.tick(delta_t)
            actor.draw(screen)
        pygame.display.flip()


if __name__ == '__main__':
    main()
