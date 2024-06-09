import pygame

class Computer:
    def __init__(self, x, y, color, width, height):
        """
        Инициализация компьютера
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20
        self.speed = 1 # скорость компьютера
        self.width = width
        self.height = height
        self.original_x = x
        self.original_y = y
        self.facing = -1

    def should_hit(self, puck):
        """
        Проверка должен ли компьютер ударить по шайбе (чем ближе к воротам)
        """
        return abs(self.x - puck.x) < 100 and self.facing == -1

    def draw(self, screen):
        """
        Отрисовка модели компьютера на площадке
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, puck):
        """
        Перемещение компьютера за шайбой
        """
        if puck.x < self.x:
            self.x -= self.speed
        elif puck.x > self.x:
            self.x += self.speed
        
        if puck.y < self.y:
            self.y -= self.speed
        elif puck.y > self.y:
            self.y += self.speed

        self.x = max(self.radius, min(self.x, self.width - self.radius))
        self.y = max(self.radius, min(self.y, self.height - self.radius))

    def reset(self):
        """
        Возврат компьютера в исходное положение
        """
        self.x = self.original_x
        self.y = self.original_y
