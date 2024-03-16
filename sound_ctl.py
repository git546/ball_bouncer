from pydub import AudioSegment
import simpleaudio as sa
import threading
import time
from pydub.utils import which
import os 

ffmpeg_path = r'C:\ffmpeg-2024-03-07-git-97beb63a66-full_build\bin'  # 여기서 경로는 실제 ffmpeg 설치 경로로 변경해야 합니다.
os.environ['PATH'] += os.pathsep + ffmpeg_path

class StreamingMusicPlayer:
    def __init__(self, filepath):
        self.audio = AudioSegment.from_file(filepath)
        self.playback_object = None
        self.current_position = 0  # 현재 재생 위치 (밀리초 단위)
        self.is_playing = False
        self.is_paused = False
        self.lock = threading.Lock()

    def play(self):
        with self.lock:
            if not self.is_playing:
                self.is_playing = True
                threading.Thread(target=self._playback_thread).start()
            elif self.is_paused:
                self.is_paused = False
                self.playback_object.stop()

    def _playback_thread(self):
        while self.current_position < len(self.audio) and self.is_playing:
            if not self.is_paused:
                segment = self.audio[self.current_position:]
                self.playback_object = sa.play_buffer(segment.raw_data, num_channels=segment.channels,
                                                      bytes_per_sample=segment.sample_width, sample_rate=segment.frame_rate)
                start_time = time.time()
                self.playback_object.wait_done()
                elapsed_time = (time.time() - start_time) * 1000  # 밀리초 단위로 변환
                self.current_position += int(elapsed_time)
            else:
                time.sleep(0.1)  # 일시 정지 상태에서는 대기

    def pause(self):
        with self.lock:
            if self.is_playing and not self.is_paused:
                self.is_paused = True
                self.playback_object.stop()

    def stop(self):
        with self.lock:
            self.is_playing = False
            self.current_position = 0
            if self.playback_object:
                self.playback_object.stop()

if __name__ == "__main__":
    player = StreamingMusicPlayer("./sample.mp3")  # 여러분의 오디오 파일 경로로 변경하세요.
    player.play()
    time.sleep(10)  # 5초 동안 재생
    player.pause()
    print("일시 정지...")
    time.sleep(3)  # 3초 동안 일시 정지
    print("재개...")
    player.play()
    time.sleep(5)  # 다시 5초 동안 재생
    player.stop()
    print("정지 및 종료...")
