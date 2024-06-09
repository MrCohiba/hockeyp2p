import pygame

class Client:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.Font(None, 36)
        self.play_button = pygame.Rect(300, 400, 200, 50)

    def draw(self):
        """
        Визуализация меню и кнопки играть
        """
        self.draw_menu()
        self.draw_play_button()

    def draw_menu(self):
        """
        Заголовок меню
        """
        title_font = pygame.font.Font(None, 72)
        title_text = title_font.render("HOCKEY", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(400, 200))
        self.screen.blit(title_text, title_rect)

    def draw_play_button(self):
        """
        Кнопка играть
        """
        pygame.draw.rect(self.screen, (0, 128, 0), self.play_button)
        pygame.draw.rect(self.screen, (255, 255, 255), self.play_button, 2)
        play_text = self.font.render("ИГРАТЬ", True, (255, 255, 255))
        play_rect = play_text.get_rect(center=self.play_button.center)
        self.screen.blit(play_text, play_rect)
