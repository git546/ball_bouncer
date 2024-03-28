import pygame
import sys
from pygame import gfxdraw
import random
from game_configurations import configurations
from game_configurations import colors

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

def lerp_color(start_color, end_color, t):
    """
    선형 보간을 사용하여 두 색상 사이의 중간 색상을 계산합니다.
    :param start_color: 시작 색상 (R, G, B)
    :param end_color: 끝 색상 (R, G, B)
    :param t: 보간 비율 (0.0 ~ 1.0)
    :return: 보간된 중간 색상 (R, G, B)
    """
    r = start_color[0] + (end_color[0] - start_color[0]) * t
    g = start_color[1] + (end_color[1] - start_color[1]) * t
    b = start_color[2] + (end_color[2] - start_color[2]) * t
    return int(r), int(g), int(b)

class ColorFadeGimmick:
    def __init__(self):
        self.rainbow_colors = [colors['red'], colors['orange'], colors['yellow'],
                               colors['green'], colors['blue'], colors['indigo'], colors['violet']]
        self.current_index = 0
        self.t = 0.0  # 현재 보간 비율

    def apply(self, ball, border, game):
        # 현재 색상과 다음 색상 계산
        start_color = self.rainbow_colors[self.current_index]
        end_color = self.rainbow_colors[(self.current_index + 1) % len(self.rainbow_colors)]
        
        # 보간된 색상 적용
        interpolated_color = lerp_color(start_color, end_color, self.t)
        ball.set_border_color(interpolated_color)
        
        # 보간 비율 업데이트
        self.t += 0.005  # 보간 속도 조절
        if self.t >= 1.0:
            self.t = 0.0
            self.current_index = (self.current_index + 1) % len(self.rainbow_colors)

class BorderToggleGimmick(GimmickStrategy):#테두리 만드는 기믹
    def apply(self, ball, border, game):
        ball.show_border = not ball.show_border  # 테두리 표시 여부를 토글

class Ball:
    def __init__(self, position, speed, radius, color, growth, energy_loss, gravity):
        self.position = pygame.math.Vector2(position)
        self.speed = pygame.math.Vector2(speed)
        self.radius = radius
        self.color = color
        self.growth = growth
        self.energy_loss = energy_loss
        self.gravity = gravity
        self.show_border = False  # 테두리 표시 여부를 저장하는 변수
        self.border_color = colors['red']

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
            
    def set_border_color(self, value):
        if all(0 <= channel <= 255 for channel in value):
            self.border_color = value
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
        if self.show_border:
           pygame.draw.circle(screen, self.border_color, (int(self.position.x), int(self.position.y)), self.radius*1.5)            # 테두리를 그리는 로직 추가
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
        
        self.initialize_gimmicks(selected_type.get('gimmick', {}))
        
        print(self.gimmicks_on_collision)
        
        for gimmick in self.gimmicks_on_collision:
            gimmick.apply(self.ball, self.border, self)
    
    def set_background_color(self, value):
            if all(0 <= channel <= 255 for channel in value):
                self._background_color = value
            else:
                print("Each channel in the background color must be between 0 and 255.")
                
    def initialize_gimmicks(self, gimmick_config):
        # 충돌 시와 이동 시 적용되는 기믹 객체 리스트 초기화
        self.gimmicks_on_collision = []
        self.gimmicks_on_move = []
        self.gimmicks_on_init = []
        
        #초기화 시 적용되는 기믹 초기화
        for gimmick_name, is_on in gimmick_config.get('on_init', {}).items():
            if is_on:
                gimmick_class = globals().get(gimmick_name)
                if gimmick_class:
                    self.gimmicks_on_init.append(gimmick_class())
        # 충돌 시 적용되는 기믹 초기화
        for gimmick_name, is_on in gimmick_config.get('on_collision', {}).items():
            if is_on:
                gimmick_class = globals().get(gimmick_name)
                if gimmick_class:
                    self.gimmicks_on_collision.append(gimmick_class())

        # 이동 시 적용되는 기믹 초기화
        for gimmick_name, is_on in gimmick_config.get('on_move', {}).items():
            if is_on:
                gimmick_class = globals().get(gimmick_name)
                if gimmick_class:
                    self.gimmicks_on_move.append(gimmick_class())
        
                            
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
                    
            for gimmick in self.gimmicks_on_init:
                gimmick.apply(self.ball, self.border, self)
                # 이후 이 리스트를 비워서 다시 적용되지 않도록 함
            self.gimmicks_on_init = []

            self.ball.move()
            if self.ball.bounce(self.border):
                #self.selected_gimmick.apply(self.ball, self.border, self)
                for gimmick in self.gimmicks_on_collision:
                    gimmick.apply(self.ball, self.border, self)


            for gimmick in self.gimmicks_on_move:
                gimmick.apply(self.ball, self.border, self)
                
            self.screen.fill(self._background_color)
            self.border.draw(self.screen)
            self.ball.draw(self.screen)
            pygame.display.flip()

            clock.tick(60)


if __name__ == "__main__":
    game = Game()
    game.run()
