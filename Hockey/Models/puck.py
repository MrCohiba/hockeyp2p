import pygame

class Puck:
    def __init__(self, x, y, width, height):
        """
        Инициализация шайбы
        """
        self.x = x
        self.y = y
        self.radius = 10
        self.speed_x = 0
        self.speed_y = 0
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        self.owner = None
        self.hit_speed = 10

    def hit(self, direction):
        """
        Удар по шайбе
        """
        self.speed_x = direction * self.hit_speed # направление удара
        self.speed_y = 0
        self.owner = None

    def reset(self):
        """
        Возврат шайбы в исходное положение
        """
        self.x = self.original_x
        self.y = self.original_y
        self.speed_x = 0
        self.speed_y = 0
        self.owner = None
        
    def draw(self, screen):
        """
        Отрисовка шайбы
        """
        pygame.draw.circle(screen, (0, 0, 0), (self.x, self.y), self.radius)

    def update(self):
        """
        Обновление позиции шайбы на площадке
        """
        if self.owner:
            self.x = self.owner.x
            self.y = self.owner.y
        else:
            self.x += self.speed_x
            self.y += self.speed_y
            self.check_boundaries()

    def check_boundaries(self):
        """
        Проверка столкновения шайбы с бортами
        """
        if self.x <= 55 and not (self.height // 2 - 50 <= self.y <= self.height // 2 + 50):
            self.x = 55
            self.speed_x = -self.speed_x
        elif self.x >= self.width - 55 and not (self.height // 2 - 50 <= self.y <= self.height // 2 + 50):
            self.x = self.width - 55
            self.speed_x = -self.speed_x
        
        if self.y <= 55:
            self.y = 55
            self.speed_y = -self.speed_y
        elif self.y >= self.height - 55:
            self.y = self.height - 55
            self.speed_y = -self.speed_y

    def check_collision(self, player):
        """
        Проверка столкновения шайбы с игроком
        """
        dx = self.x - player.x
        dy = self.y - player.y
        distance = (dx ** 2 + dy ** 2) ** 0.5
        if distance <= self.radius + player.radius:
            if distance != 0:
                self.speed_x = dx / distance * 10
                self.speed_y = dy / distance * 10
            else:
                self.speed_x = 0
                self.speed_y = 0
