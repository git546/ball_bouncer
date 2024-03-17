import cv2
import pygame
import sys
import threading
import subprocess
from pygame.math import Vector2
import ball_bounce
import pyaudio
import wave

# 오디오 녹음을 위한 설정
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024
OUTPUT_FILENAME = "audio.wav"
audio = pyaudio.PyAudio()
frames = []

def improve_video_quality(input_video, output_video):
    # 비트레이트를 증가시키고 해상도를 유지하여 비디오 품질 개선
    command = [
        'ffmpeg',
        '-i', input_video,
        '-b:v', '2M',  # 비디오 비트레이트를 2Mbps로 설정
        '-vcodec', 'libx264',
        '-preset', 'slow',
        '-crf', '0',  # 품질 수준 설정 (0~51, 낮을수록 높은 품질)
        output_video
    ]
    subprocess.run(command)

def increase_audio_volume(input_audio, output_audio, volume_factor=20.0):
    # 오디오 볼륨 조정
    command = [
        'ffmpeg',
        '-i', input_audio,
        '-filter:a', f"volume={volume_factor}",
        output_audio
    ]
    subprocess.run(command)
    
def record_audio():
    stream = audio.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
    while running:
        data = stream.read(CHUNK)
        frames.append(data)
    stream.stop_stream()
    stream.close()
    audio.terminate()
    wf = wave.open(OUTPUT_FILENAME, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

# 오디오 녹음 스레드 시작
audio_thread = threading.Thread(target=record_audio)
audio_thread.start()

# 비디오 녹화 설정 및 게임 루프
pygame.init()
width, height = 900, 600
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Bouncing Ball Simulation with Video Recording')
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
fps = 60
video = cv2.VideoWriter('video.mp4', fourcc, fps, (width, height))

running = True
while running:
    ball_bounce.bounce_process()  # bounce_process 함수가 screen 객체를 필요로 한다고 가정
    pygame.display.flip()
    frame = pygame.surfarray.array3d(pygame.display.get_surface())
    frame = cv2.transpose(frame)
    frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
    video.write(frame)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

video.release()
pygame.quit()

# 오디오 녹음 스레드 종료 대기
audio_thread.join()

improve_video_quality('video.mp4', 'video.mp4')
increase_audio_volume('audio.wav', 'audio.wav')
# 비디오와 오디오 파일 합치기
command = ['ffmpeg', '-i', 'video.mp4', '-i', 'audio.wav', '-c:v', 'copy', '-c:a', 'aac', 'final_output.mp4']
subprocess.run(command)
