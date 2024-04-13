import pygame
import pygame.mixer
from pygame import gfxdraw
import sys
import random
import threading
from pydub import AudioSegment
import simpleaudio as sa
import time
import os
import pyaudio
import wave

from game_configurations import configurations
from game_configurations import colors

ffmpeg_path = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'  # 여기서 경로는 실제 ffmpeg 설치 경로로 변경해야 합니다.
os.environ['PATH'] += os.pathsep + ffmpeg_path

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

class ColorFadeGimmick(GimmickStrategy):
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
        ball.color = interpolated_color
        border.outer_color = interpolated_color
        
        # 보간 비율 업데이트
        self.t += 0.005  # 보간 속도 조절
        if self.t >= 1.0:
            self.t = 0.0
            self.current_index = (self.current_index + 1) % len(self.rainbow_colors)

class BorderToggleGimmick(GimmickStrategy):#테두리 만드는 기믹
    def apply(self, ball, border, game):
        ball.show_border = not ball.show_border  # 테두리 표시 여부를 토글
        
class Tracer_Gimmick(GimmickStrategy):#트레이서를 만드는 기믹
    def apply(self, ball, border, game):
        border.is_inner = False  # 더 이상 공 내부를 갱신하지 않도록 토글


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

class SoundGimmick(GimmickStrategy):
    def __init__(self, sound_file):
        self.sound_file = sound_file
        self.audio = AudioSegment.from_file(self.sound_file)
        self.playback_object = None
        self.current_position = 0  # 현재 재생 위치 (밀리초 단위)
        self.is_playing = False
        self.is_paused = False
        self.lock = threading.Lock()

    def play(self):
        with self.lock:
            if not self.is_playing or self.is_paused:
                self.is_playing = True
                self.is_paused = False
                threading.Thread(target=self._playback_thread).start()

    def _playback_thread(self):
        while self.current_position < len(self.audio) and self.is_playing:
            if not self.is_paused:
                segment = self.audio[self.current_position:]
                self.playback_object = sa.play_buffer(segment.raw_data, num_channels=segment.channels,
                                                      bytes_per_sample=segment.sample_width, sample_rate=segment.frame_rate)
                start_time = time.time()
                self.playback_object.wait_done()
                elapsed_time = (time.time() - start_time) * 1000
                self.current_position += int(elapsed_time)
            else:
                time.sleep(0.1)

    def pause(self):
        with self.lock:
            if self.is_playing and not self.is_paused:
                self.is_paused = True
                if self.playback_object:
                    self.playback_object.stop()

    def stop(self):
        with self.lock:
            if self.playback_object:
                self.playback_object.stop()
            self.is_playing = False
            self.current_position = 0

    def play_segment_async(self, duration_ms=1000):
        threading.Thread(target=self._play_segment, args=(duration_ms,)).start()

    def _play_segment(self, duration_ms):
        with self.lock:
            if not self.is_playing:
                if self.current_position + duration_ms > len(self.audio):
                    duration_ms = len(self.audio) - self.current_position
                segment = self.audio[self.current_position:self.current_position + duration_ms]
                self.playback_object = sa.play_buffer(segment.raw_data, num_channels=segment.channels, bytes_per_sample=segment.sample_width, sample_rate=segment.frame_rate)
                #self.playback_object.wait_done()
                self.current_position += duration_ms
                if self.current_position >= len(self.audio):
                    self.current_position = 0  # 끝에 도달했으니 처음부터 다시 시작

    def apply(self, ball, border, game):
        # 예: 게임에서 특정 이벤트 발생 시 음악 재생
        if not self.is_playing:
            self.play()
        elif self.is_paused:
            self.play()  # 일시 정지된 상태에서는 다시 재생
        else:
            # 재생 중에 다른 이벤트 발생 시 (예를 들어, 다른 특정 상황) 일시 정지 또는 정지 등의 조치를 취할 수 있음
            pass

class SoundRecorder:
    def __init__(self, output_filename):
        self.chunk = 1024
        self.format = pyaudio.paInt16
        self.channels = 1  # 모노로 설정
        self.sample_rate = 44100
        self.frames = []
        self.output_filename = output_filename
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format=self.format,
                                  channels=self.channels,
                                  rate=self.sample_rate,
                                  input=True,
                                  frames_per_buffer=self.chunk)

    def start(self):
        self.is_recording = True
        thread = threading.Thread(target=self.record)
        thread.start()

    def stop(self):
        self.is_recording = False
        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
        self.save_recording()

    def record(self):
        while self.is_recording:
            data = self.stream.read(self.chunk)
            self.frames.append(data)

    def save_recording(self):
        wave_file = wave.open(self.output_filename, 'wb')
        wave_file.setnchannels(self.channels)
        wave_file.setsampwidth(self.p.get_sample_size(self.format))
        wave_file.setframerate(self.sample_rate)
        wave_file.writeframes(b''.join(self.frames))
        wave_file.close()

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
        self.is_inner = True
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
        if self.is_inner:
            # 외부 원 그리기
            pygame.draw.circle(screen, self.outer_color, self.center, self.radius + self.thickness)
            # 내부 원 그리기
            pygame.draw.circle(screen, self.inner_color, self.center, self.radius)

class Game:
    def __init__(self):
        #프로그램 초시화, pygame과 사운드 초기화
        pygame.init()
        pygame.mixer.init()
        
        #오디오 파일 생성
        self.recorder = SoundRecorder('game_audio.wav')
        self.recorder.start()  # 게임 시작 시 녹음 시작

        #화면 크기 초기화 및 창 이름 설정
        self.width, self.height = 1080, 1920
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Bouncing Ball Simulation with Classes')
        
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        
        self._background_color = self.black
        
        # 랜덤으로 유형 선택
        selected_type_key = random.choice(list(configurations.keys()))
        selected_type_key = 'line-bouncing' #임의로 설정하는 테스트용 명령
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
        
        print(self.gimmicks_on_move)
        
     
        # 다른 초기화 코드...
        
        # SoundGimmick 초기화
        sound_file = "Queencards.mp3"  # 소리 파일 경로
        self.sound_gimmick = SoundGimmick(sound_file)
        
        # 기존의 gimmicks_on_collision 리스트에 추가
        self.gimmicks_on_collision.append(self.sound_gimmick)
    
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
                    
            if self.border.is_inner:
                self.screen.fill(self._background_color)
                
            self.border.draw(self.screen)
            self.ball.draw(self.screen)
                
            self.ball.move()
            
            if self.ball.bounce(self.border):
                for gimmick in self.gimmicks_on_move:
                    if isinstance(gimmick, ConnectGimmick):  # ConnectGimmick에만 해당s
                        gimmick.add(self.ball, self.border, self)
                for gimmick in self.gimmicks_on_collision:
                    gimmick.apply(self.ball, self.border, self)
                


            for gimmick in self.gimmicks_on_move:
                gimmick.apply(self.ball, self.border, self)
            
            pygame.display.flip()
            
            for gimmick in self.gimmicks_on_init:
                gimmick.apply(self.ball, self.border, self)
            self.gimmicks_on_init = [] # 이후 이 리스트를 비워서 다시 적용되지 않도록 함
            
            if self.ball.get_radius()>1000:
                return
            
            clock.tick(60)
    def close(self):
        self.recorder.stop()  # 게임 종료 시 녹음 중지


if __name__ == "__main__":
    
    while 1:
        game = Game()
        game.run()
        game.close()
