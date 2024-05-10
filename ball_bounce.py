import pygame
import pygame.mixer
from pygame import gfxdraw
import random

import time
import os

import cv2
import numpy as np

from game_configurations import configurations
from game_configurations import colors

ffmpeg_path = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'  # 여기서 경로는 실제 ffmpeg 설치 경로로 변경해야 합니다.
os.environ['PATH'] += os.pathsep + ffmpeg_path
os.environ["SDL_VIDEODRIVER"] = "dummy"

class GimmickStrategy:
    def apply(self, ball, border, game):
        pass

class EchoGimmick(GimmickStrategy):
    def __init__(self, echo_lifetime=200):
        self.echo_lifetime = echo_lifetime
        self.echoes = []

    def apply(self, ball, border, game):
        self.echoes.append((ball.position.copy(), self.echo_lifetime))
        new_echoes = []
        for position, lifetime in self.echoes:
            if lifetime > 0:
                new_echoes.append((position, lifetime - 1))
        self.echoes = new_echoes

    def draw(self, ball, border, game):
        for position, lifetime in self.echoes:
            alpha = int(255 * (lifetime / self.echo_lifetime))
            echo_color = ball.color + (alpha,)
            pygame.draw.circle(game, echo_color, (int(position.x), int(position.y)), ball.radius)
            
class ColorSwapGimmick(GimmickStrategy):
    def apply(self, ball, border, game):
    
        border_inner_color = border.inner_color
        border_outer_color = border.outer_color
        
        game._background_color = border_outer_color
        border.outer_color=border_inner_color
        border.inner_color=border_outer_color
        ball.set_color(border_inner_color)
        

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

class ColorFadeGimmick(GimmickStrategy):
    def __init__(self):
        self.rainbow_colors = [colors['red'], colors['orange'], colors['yellow'],
                               colors['green'], colors['blue'], colors['indigo'], colors['violet']]
        self.current_index = 0
        self.t = 0.0  # 현재 보간 비율

    def interpolate_color(self):
        # 현재 색상과 다음 색상 계산
        start_color = self.rainbow_colors[self.current_index]
        end_color = self.rainbow_colors[(self.current_index + 1) % len(self.rainbow_colors)]
        # 보간된 색상 적용
        interpolated_color = lerp_color(start_color, end_color, self.t)
        return interpolated_color

    def update_color_index(self):
        self.t += 0.005  # 보간 속도 조절
        if self.t >= 1.0:
            self.t = 0.0
            self.current_index = (self.current_index + 1) % len(self.rainbow_colors)

class BorderFadeGimmick(ColorFadeGimmick):
    def apply(self, ball, border, game):
        interpolated_color = self.interpolate_color()
        border.outer_color = interpolated_color
        self.update_color_index()

class BallFadeGimmick(ColorFadeGimmick):
    def apply(self, ball, border, game):
        interpolated_color = self.interpolate_color()
        ball.color = interpolated_color
        self.update_color_index()

class BallBorderFadeGimmick(ColorFadeGimmick):
    def apply(self, ball, border, game):
        interpolated_color = self.interpolate_color()
        ball.border_color = interpolated_color
        self.update_color_index()

class BackgroundFadeGimmick(ColorFadeGimmick):
    def apply(self, ball, border, game):
        interpolated_color = self.interpolate_color()
        game.set_background_color(interpolated_color)
        self.update_color_index()


class BorderToggleGimmick(GimmickStrategy):#테두리 만드는 기믹
    def apply(self, ball, border, game):
        ball.show_border = not ball.show_border  # 테두리 표시 여부를 토글
        
class Tracer_Gimmick(GimmickStrategy):
    def __init__(self, trace_length=20):
        self.traces = []
        self.trace_length = trace_length

    def apply(self, ball, border, game):
        if len(self.traces) >= self.trace_length:
            self.traces.pop(0)
        self.traces.append({
            'position': ball.position.copy(),
            'color': ball.color,
            'radius': ball.radius
        })
        self.draw(game)
        
    def draw(self, game):
        for trace in self.traces:
            alpha = int(255 * (self.traces.index(trace) + 1) / len(self.traces))
            trace_surface = pygame.Surface((game.width, game.height), pygame.SRCALPHA)
            trace_color = trace['color'] + (alpha,)
            pygame.gfxdraw.filled_circle(trace_surface, int(trace['position'].x), int(trace['position'].y), trace['radius'], trace_color)
            pygame.gfxdraw.aacircle(trace_surface, int(trace['position'].x), int(trace['position'].y), trace['radius'], trace_color)
            game.screen.blit(trace_surface, (0, 0))

class PermanentTracerGimmick(GimmickStrategy):
    def __init__(self):
        self.traces = []

    def apply(self, ball, border, game):
        # 공의 현재 위치를 복사하여 흔적 목록에 추가
        self.traces.append({
            'position': ball.position.copy(),
            'color': ball.color,
            'radius': ball.radius,
            'border': ball.border_color,
        })
        self.draw(game.screen, ball)

    def draw(self, screen, ball):
        for trace in self.traces:
            trace_color = trace['color'] + (255,)  # 완전 불투명
            trace_border_color = trace['border'] + (255,)
            if ball.show_border : 
                pygame.gfxdraw.filled_circle(screen, int(trace['position'].x), int(trace['position'].y), trace['radius'] + 2, trace_border_color)
            pygame.gfxdraw.filled_circle(screen, int(trace['position'].x), int(trace['position'].y), trace['radius'], trace_color)
            pygame.gfxdraw.aacircle(screen, int(trace['position'].x), int(trace['position'].y), trace['radius'], trace_color)


class ConnectGimmick(GimmickStrategy):
    def __init__(self):
        self.collision_point_list = []

    def apply(self, ball, border, game):
        for point in self.collision_point_list:
            pygame.draw.line(game.screen, ball.color, (int(point.x), int(point.y)), ball.position, 2)

    def add(self, ball, border, game):
        direction = ball.position - border.center
        distance = direction.length()
        normal = direction.normalize()
        overlap = distance - border.radius
        collision_point = ball.position - overlap * normal  # 충돌 지점 계산
        if collision_point:
            self.collision_point_list.append(collision_point)

class CollisionRecorderGimmick:
    def __init__(self):
        self.collision_times = []
        self.start_time = time.time() * 1000  # 시작 시간을 밀리초로 변환

    def record_collision(self):
        current_time = time.time() * 1000  # 현재 시간을 밀리초로 변환
        collision_time = current_time - self.start_time
        self.collision_times.append(collision_time)

    def get_collision_times(self):
        return self.collision_times

    def apply(self, ball, border, game):
            self.record_collision()
            
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
        self.border_color = colors['white']

    # Speed setter
    def set_speed(self, value):
        self.speed = pygame.math.Vector2(value)

    # Radius setter
    def set_radius(self, value):
        if value > 0:
            self.radius = value
        else:
            print("Radius must be positive.")
            
    def get_radius(self):
        return self.radius
    
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
            #print("bounce\n")
            return True

        return False

    def draw(self, screen):
        if self.show_border:
           pygame.draw.circle(screen, self.border_color, (int(self.position.x), int(self.position.y)), self.radius+3)            # 테두리를 그리는 로직 추가
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
        #프로그램 초시화, pygame과 사운드 초기화
        pygame.init()
        pygame.mixer.init()
        
        # 랜덤으로 유형 선택
        selected_type_key = random.choice(list(configurations.keys()))
        selected_type_key = 'fade_color_tracing' #임의로 설정하는 테스트용 명령
        selected_type = configurations[selected_type_key]
        
        # Game setting 초기화
        game_settings = selected_type['Game_setting']
        self.width = game_settings['width']
        self.height = game_settings['height']
        self._background_color = game_settings['bg_color']
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Bouncing Ball Simulation with Classes')
        
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
        
        self.fourcc = cv2.VideoWriter_fourcc(*'XVID')
        self.video = cv2.VideoWriter('game_video.avi', self.fourcc, 60, (self.width, self.height), True)
    
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
        
        self.collision_recorder = CollisionRecorderGimmick()
        self.gimmicks_on_collision.append(self.collision_recorder)
        
                            
    def swap_border_and_background_colors(self):
        # 배경색과 보더색 교환
        self.border.outer_color, self._background_color = self._background_color, self.border.outer_color
    
    def run(self):
        clock = pygame.time.Clock()
        
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    
            self.screen.fill(self._background_color)
            
            self.border.draw(self.screen)
            
            pygame.display.flip()
            
            
            if self.ball.bounce(self.border):
                for gimmick in self.gimmicks_on_move:
                    if isinstance(gimmick, ConnectGimmick):  # ConnectGimmick에만 해당s
                        gimmick.add(self.ball, self.border, self)
                for gimmick in self.gimmicks_on_collision:
                    gimmick.apply(self.ball, self.border, self)
                


            for gimmick in self.gimmicks_on_move:
                gimmick.apply(self.ball, self.border, self)
            
            
            
            for gimmick in self.gimmicks_on_init:
                gimmick.apply(self.ball, self.border, self)
            self.gimmicks_on_init = [] # 이후 이 리스트를 비워서 다시 적용되지 않도록 함
            
            
            self.ball.draw(self.screen)
            self.ball.move()
            
            # Capture the frame
            frame = np.array(pygame.surfarray.array3d(self.screen))
            frame = cv2.transpose(frame)
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # Convert it to BGR
            self.video.write(frame)  # Write frame to video

            
            pygame.display.flip()
            
            if self.ball.get_radius()>10000:
                break
            
            clock.tick(60)
            
        self.video.release()    
        pygame.quit()


if __name__ == "__main__":
        game = Game()
        game.run()
