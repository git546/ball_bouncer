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
        
        self.border = Border((self.width // 2, self.height // 2), min(self.width, self.height) // 2, 1, self.white)
        self.ball = Ball((self.width // 2, self.height // 3), (3, 3), 10, self.white, 1.1, 1.01)

    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.ball.move()
            self.ball.bounce(self.border)

            self.screen.fill(self.black)
            self.border.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)

if __name__ == "__main__":
    game = Game()
    game.run()
