import pygame
import sys
from pygame import gfxdraw

class Ball:
    def __init__(self, position, speed, radius, color, growth, energy_loss):
        self.position = pygame.math.Vector2(position)
        self.speed = pygame.math.Vector2(speed)
        self.radius = radius
        self.color = color
        self.growth = growth
        self.energy_loss = energy_loss
        self.gravity = pygame.math.Vector2(0, 0.5)
    # Speed setter
    def set_speed(self, value):
        self.speed = pygame.math.Vector2(value)

    # Radius setter
    def set_radius(self, value):
        if value > 0:
            self.radius = value
        else:
            print("Radius must be positive.")
     # Color setter
    def set_color(self, value):
        if all(0 <= channel <= 255 for channel in value):
            self.color = value
        else:
            print("Each channel in the color must be between 0 and 255.")
            
    # Growth setter
    def set_growth(self, value):
        if value >= 1:
            self.growth = value
        else:
            print("Growth factor must be greater than or equal to 1.")

    # Energy loss setter
    def set_energy_loss(self, value):
        if 0 <= value <= 1:
            self.energy_loss = value
        else:
            print("Energy loss must be between 0 and 1.")
            
    def move(self):
        self.speed += self.gravity
        self.position += self.speed

    def bounce(self, border):
        direction = self.position - border.center
        distance = direction.length()

        if distance >= border.radius - self.radius:
            normal = direction.normalize()
            self.speed.reflect_ip(normal)
            self.speed *= self.energy_loss
            self.radius = int(self.radius * self.growth)
            
            
            if self.color != (0,0,0):
                self.color = (0,0,0)
                Game.set_background_color(Game,(255,255,255))
            else :
                self.color = (255,255,255)
                Game.set_background_color(Game,(0,0,0))
            
            overlap = distance + self.radius - border.radius
            self.position -= overlap * normal

    def draw(self, screen):
        gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.radius, self.color)
        gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.radius, self.color)

class Border:
    def __init__(self, center, radius, thickness, color):
        self.center = pygame.math.Vector2(center)
        self.radius = radius
        self.thickness = thickness
        self.color = color
    @property
    def center(self):
        return self._center

    @center.setter
    def center(self, value):
        self._center = pygame.math.Vector2(value)

    @property
    def radius(self):
        return self._radius

    @radius.setter
    def radius(self, value):
        if value > 0:
            self._radius = value
        else:
            print("Radius must be positive.")

    @property
    def thickness(self):
        return self._thickness

    @thickness.setter
    def thickness(self, value):
        if value >= 0:
            self._thickness = value
        else:
            print("Thickness must be non-negative.")

    @property
    def color(self):
        return self._color

    @color.setter
    def color(self, value):
        if all(0 <= channel <= 255 for channel in value):
            self._color = value
        else:
            print("Each channel in the color must be between 0 and 255.")

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, self.center, self.radius, self.thickness)

class Game:
    def __init__(self):
        pygame.init()
        
        self.width, self.height = 900, 600
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Bouncing Ball Simulation with Classes')
        
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (255, 0, 0)
        
        self._background_color = self.black
        self.border = Border((self.width // 2, self.height // 2), min(self.width, self.height) // 2, 1, self.white)
        self.ball = Ball((self.width // 2, self.height // 3), (3, 3), 10, self.white, 1.1, 1.01)
    
    def set_background_color(self, value):
        if all(0 <= channel <= 255 for channel in value):
            self._background_color = value
        else:
            print("Each channel in the background color must be between 0 and 255.")
    
    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.ball.move()
            self.ball.bounce(self.border)

            self.screen.fill(self._background_color)
            self.border.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
