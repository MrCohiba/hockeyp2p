import pygame

class Player:
    def __init__(self, x, y, color, width, height):
        """
        Инициализация игрока
        """
        self.x = x
        self.y = y
        self.color = color
        self.radius = 20
        self.speed = 5 # скорость игрока
        self.original_x = x
        self.original_y = y
        self.width = width
        self.height = height
        self.facing = 1 
    
    def reset(self):
        """
        Возврат игрока в начальное положение после конца раунда или матча
        """
        self.x = self.original_x
        self.y = self.original_y

    def draw(self, screen):
        """
        Отрисовка игрока на площадке
        """
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radius)

    def move(self, dx, dy):
        """
        Перемещение игрока
        """
        new_x = max(55, min(self.x + dx * self.speed, self.width - 55))
        new_y = max(55, min(self.y + dy * self.speed, self.height - 55))
        
        if 55 <= new_x <= self.width - 55 and 55 <= new_y <= self.height - 55:
            self.x = new_x
            self.y = new_y

        if dx != 0:
            self.facing = dx
