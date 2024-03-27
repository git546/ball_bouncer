import pygame
import sys
from pygame import gfxdraw
import random
from game_configurations import configurations

class GimmickStrategy:
    def apply(self, ball, border):
        pass

class ColorSwapGimmick(GimmickStrategy):
    def apply(self, ball, border, game):
        ball_color = ball.color
        border_inner_color = border.inner_color
        ball.set_color(border_inner_color)
        border.outer_color = border.inner_color
        game.swap_border_and_background_colors()  # 배경색과 보더색 교환 메서드 호출
        border.inner_color = ball_color
        

class Ball:
    def __init__(self, position, speed, radius, color, growth, energy_loss, gravity):
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
            
            overlap = distance + self.radius - border.radius
            self.position -= overlap * normal
            
            return True
        return False

    def draw(self, screen):
        gfxdraw.aacircle(screen, int(self.position.x), int(self.position.y), self.radius, self.color)
        gfxdraw.filled_circle(screen, int(self.position.x), int(self.position.y), self.radius, self.color)

class Border:
    def __init__(self, center, radius, thickness, inner_color, outer_color):
        self.center = pygame.math.Vector2(center)
        self.radius = radius
        self.thickness = thickness
        self.inner_color = inner_color  # 내부 색상 추가
        self.outer_color = outer_color  # 외부 색상 추가
        
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
        # 외부 원 그리기
        pygame.draw.circle(screen, self.outer_color, self.center, self.radius + self.thickness)
        # 내부 원 그리기
        pygame.draw.circle(screen, self.inner_color, self.center, self.radius)

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
        
        # 랜덤으로 유형 선택
        selected_type_key = random.choice(list(configurations.keys()))
        selected_type = configurations[selected_type_key]

        # Border 객체 초기화
        border_config = selected_type['border']
        self.border = Border(
           center=border_config['center'],
           radius=border_config['radius'],
           thickness=border_config['thickness'],
           inner_color=border_config['inner_color'],
           outer_color=border_config['outer_color']
        )
       
        # Ball 객체 초기화
        ball_config = selected_type['ball']
        self.ball = Ball(
           position=ball_config['position'],
           speed=ball_config['speed'],
           radius=ball_config['radius'],
           color=ball_config['color']() if callable(ball_config['color']) else ball_config['color'],
           growth=ball_config['growth'],
           energy_loss=ball_config['energy_loss'],
           gravity=ball_config['gravity']
        )
        
        # 사용 가능한 기믹 리스트
        self.gimmicks = [ColorSwapGimmick()]
        # 기믹 선택
        self.selected_gimmick = random.choice(self.gimmicks)
    
    def set_background_color(self, value):
        if all(0 <= channel <= 255 for channel in value):
            self._background_color = value
        else:
            print("Each channel in the background color must be between 0 and 255.")
            
    def swap_border_and_background_colors(self):
        # 배경색과 보더색 교환
        self.border.outer_color, self._background_color = self._background_color, self.border.outer_color
    
    def run(self):
        clock = pygame.time.Clock()

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            self.ball.move()
            if self.ball.bounce(self.border):
                self.selected_gimmick.apply(self.ball, self.border, self)

            self.screen.fill(self._background_color)
            self.border.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
