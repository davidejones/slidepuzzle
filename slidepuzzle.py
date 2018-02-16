import pygame


def main():
    pygame.init()
    pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Slide Puzzle')
    is_running = True
    clock = pygame.time.Clock()
    while is_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                is_running = False
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


if __name__ == '__main__':
    main()
