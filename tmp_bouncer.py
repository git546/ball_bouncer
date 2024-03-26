import pygame
import sys
import random
from pygame import gfxdraw

class GimmickStrategy:
    def apply(self, ball, border, game):
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
        
        # 랜덤으로 컬러 또는 흑백 선택
        self.color_mode = random.choice(['color', 'monochrome'])
        if self.color_mode == 'color':
            # 컬러 디자인 세트 중 하나를 랜덤으로 선택
            pass
        else:
            # 흑백 디자인 세트 선택
            pass
        
        # on/off 기믹 활성화 여부 선택
        self.gimmicks = [ColorSwapGimmick()] # 예시로 ColorSwapGimmick만 추가
        self.selected_gimmick = random.choice(self.gimmicks) # 랜덤으로 기믹 선택
        
        # 바운스 기믹 선택 (여기서는 예시로 하나만 선택)
        self.bounce_gimmick = self.selected_gimmick
        
        # 추가적인 초기화 필요한 경우 여기에 작성
        
    def run(self):
        running = True
        clock = pygame.time.Clock()
        
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            
            # 공 이동, 경계 반사 로직 등
            
            # 기믹 적용
            if self.selected_gimmick:
                self.selected_gimmick.apply(None, None, self) # 예시, 실제로는 인자로 적절한 객체 전달
            
            # 화면 그리기
            self.screen.fill((255, 255, 255)) # 예시로 하얀 배경 설정, 실제로는 선택된 디자인 적용
            # 여기에 공 그리기, 경계 그리기 등의 로직 추가
            
            pygame.display.flip()
            clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
