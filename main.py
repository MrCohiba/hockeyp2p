import pygame
from Hockey.client import Client
from Hockey.game import Game

def main():
    """
    Обработка событий и запуск игры
    """
    pygame.init()
    screen = pygame.display.set_mode((800, 600)) # размер окна
    pygame.display.set_caption("Hockey") # название окна
    clock = pygame.time.Clock()

    client = Client(screen)
    game = Game(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if client.play_button.collidepoint(event.pos):
                    game.run()
                    game.reset_game()

        screen.fill((255, 255, 255))  # Цвет фона
        client.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

