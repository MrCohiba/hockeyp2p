import pygame
from Hockey.Models.player import Player
from Hockey.Models.computer import Computer
from Hockey.Models.puck import Puck

class Game:
    def __init__(self, screen):
        """
        Инициализация игры
        """
        self.screen = screen
        self.width = 800
        self.height = 600
        self.color = (255, 255, 255)
        self.goal_color = (255, 0, 0)
        self.line_color = (0, 0, 255)
        self.center_line_color = (128, 128, 128)
        
        self.player = Player(100, self.height // 2, (0, 255, 0), self.width, self.height)
        self.computer = Computer(self.width - 100, self.height // 2, (255, 0, 0), self.width, self.height)
        self.puck = Puck(self.width // 2, self.height // 2, self.width, self.height)
        
        self.player_score = 0
        self.computer_score = 0
        self.time_remaining = 300000 # основное время матча
        self.delay_timer = 0
        self.delay_time = 3 * 60  # время задержки
        self.player_hit_cooldown = 0
        self.computer_hit_cooldown = 0
        self.hit_cooldown_time = 30  # 0.5 секунд в кадрах
        
        self.font = pygame.font.Font(None, 36)
        self.game_over_delay = 5 * 60  # 5 секунд в кадрах

    def run(self):
        """
        Главный цикл игры
        """
        clock = pygame.time.Clock()
        running = True
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        if self.player_hit_cooldown == 0:
                            self.player_hit()
                            self.player_hit_cooldown = self.hit_cooldown_time

            """
            Кейкапы игрока
            """
            keys = pygame.key.get_pressed()
            if self.delay_timer == 0:
                dx = (keys[pygame.K_d] or keys[pygame.K_v]) - (keys[pygame.K_a] or keys[pygame.K_f])
                dy = (keys[pygame.K_s] or keys[pygame.K_y]) - (keys[pygame.K_w] or keys[pygame.K_c])
                self.player.move(dx, dy)
            else:
                self.delay_timer -= 1

            if not self.game_over():
                if self.delay_timer == 0:
                    self.computer.move(self.puck)
                    if self.computer_hit_cooldown == 0 and self.computer.should_hit(self.puck):
                        self.computer_hit()
                        self.computer_hit_cooldown = self.hit_cooldown_time
                    self.puck.update()
                    self.check_puck_possession()
                    self.check_goal()
                    self.update_time()
                    self.update_cooldowns()
                else:
                    self.delay_timer -= 1

            self.draw()
            pygame.display.flip()
            clock.tick(60)

            if self.game_over():
                self.draw_game_over()
                pygame.display.flip()
                pygame.time.delay(self.game_over_delay * 1000 // 60)  # Конвертация кадров в мс
                return

    def player_hit(self):
        """
        Удар игрока
        """
        if self.puck.owner == self.player:
            self.puck.hit(self.player.facing)

    def computer_hit(self):
        """
        Удар компьютера
        """
        if self.puck.owner == self.computer:
            self.puck.hit(self.computer.facing)

    def update_cooldowns(self):
        """
        Обновление таймеров
        """
        self.player_hit_cooldown = max(0, self.player_hit_cooldown - 1)
        self.computer_hit_cooldown = max(0, self.computer_hit_cooldown - 1)

    def draw(self):
        """
        Отрисовка линий, бортов и так далее
        """
        self.screen.fill((220, 220, 220))
        self.draw_rink()
        self.player.draw(self.screen)
        self.computer.draw(self.screen)
        self.puck.draw(self.screen)
        self.draw_scores()
        self.draw_time()

    def draw_rink(self):
        """
        Хоккейная площадка (взял с вики)
        """
        pygame.draw.rect(self.screen, (0, 0, 0), (45, 45, self.width - 90, self.height - 90), 5)
        pygame.draw.rect(self.screen, self.color, (50, 50, self.width - 100, self.height - 100))
        pygame.draw.rect(self.screen, self.goal_color, (0, self.height // 2 - 50, 50, 100))
        pygame.draw.rect(self.screen, self.goal_color, (self.width - 50, self.height // 2 - 50, 50, 100))
        pygame.draw.line(self.screen, self.line_color, (50, 50), (50, self.height - 50), 5)
        pygame.draw.line(self.screen, self.line_color, (self.width - 50, 50), (self.width - 50, self.height - 50), 5)
        pygame.draw.line(self.screen, self.center_line_color, (self.width // 2, 50), (self.width // 2, self.height - 50), 2)

    def draw_scores(self):
        """
        Отрисовка счета игры
        """
        player_text = self.font.render(f"Игрок: {self.player_score}", True, (0, 0, 0))
        computer_text = self.font.render(f"Компьютер: {self.computer_score}", True, (0, 0, 0))
        self.screen.blit(player_text, (50, 10))
        self.screen.blit(computer_text, (self.width - 200, 10))

    def draw_time(self):
        """
        Отрисовка оставшегося времени
        """
        minutes = max(0, self.time_remaining // 60)
        seconds = max(0, self.time_remaining % 60)
        time_text = self.font.render(f"{minutes:02d}:{seconds:02d}", True, (0, 0, 0))
        time_rect = time_text.get_rect(center=(self.width // 2, 30))
        self.screen.blit(time_text, time_rect)

    def draw_game_over(self):
        """
        Отрисовка окончания игры
        """
        if self.player_score == self.computer_score:
            result_text = self.font.render("НИЧЬЯ!", True, (0, 0, 0))
        else:
            winner = "Игрок" if self.player_score > self.computer_score else "Компьютер"
            result_text = self.font.render(f"ПОБЕДИЛ: {winner}!", True, (0, 0, 0))
        
        game_over_text = self.font.render("ИГРА ЗАКОНЧЕНА", True, (0, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.width // 2, self.height // 2 - 20))
        result_rect = result_text.get_rect(center=(self.width // 2, self.height // 2 + 20))
        self.screen.blit(game_over_text, game_over_rect)
        self.screen.blit(result_text, result_rect)

    def check_goal(self):
        """
        Проверка забитых голов
        """
        if self.puck.x <= 50 and self.height // 2 - 50 <= self.puck.y <= self.height // 2 + 50:
            self.computer_score += 1
            self.reset_positions()
        elif self.puck.x >= self.width - 50 and self.height // 2 - 50 <= self.puck.y <= self.height // 2 + 50:
            self.player_score += 1
            self.reset_positions()

    def check_puck_possession(self):
        """
        Проверка владения шайбой
        """
        if self.puck.check_collision(self.player):
            self.puck.owner = self.player
        elif self.puck.check_collision(self.computer):
            self.puck.owner = self.computer

    def reset_positions(self):
        """
        Сброс позиций модели игроков и шайбы
        """
        self.player.reset()
        self.computer.reset()
        self.puck.reset()
        self.delay_timer = self.delay_time


    def update_time(self):
        """
        Обновление оставшегося времени игры
        """
        if self.time_remaining > 0:
            self.time_remaining -= 1

    def game_over(self):
        """
        Проверка окончания игры
        """
        if self.time_remaining <= 0:
            return True
        elif self.player_score == 10 or self.computer_score == 10:
            return True
        else:
            return False

    def reset_game(self):
        """
        Сброс игры
        """
        self.player_score = 0
        self.computer_score = 0
        self.time_remaining = 300000
        self.reset_positions()
