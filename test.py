import pyaudio
import wave
from pydub import AudioSegment

# 오디오 파일 불러오기 및 처리
audio = AudioSegment.from_file("80s-radio-tune-113798.mp3")

# 오디오의 5초부터 10초까지 잘라내기
clip = audio[5000:10000]

# 1초간의 무음 추가
silence = AudioSegment.silent(duration=1000)  # 1000ms = 1초
audio_with_gaps = clip + silence + clip  # 무음을 추가하여 두 클립 사이에 삽입

# PyAudio 설정
FORMAT = pyaudio.paInt16
CHANNELS = audio_with_gaps.channels
RATE = audio_with_gaps.frame_rate
CHUNK = 1024

# 파일로 출력 준비
WAVE_OUTPUT_FILENAME = "output_with_gaps.wav"
wf = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
wf.setnchannels(CHANNELS)
wf.setsampwidth(pyaudio.PyAudio().get_sample_size(FORMAT))
wf.setframerate(RATE)

# PyAudio 객체 초기화
p = pyaudio.PyAudio()

# 스트림 열기
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, output=True, frames_per_buffer=CHUNK)

# AudioSegment에서 raw audio data를 얻기
raw_data = audio_with_gaps.raw_data

# 데이터를 스트림에 쓰기 및 파일에 저장
for i in range(0, len(raw_data), CHUNK):
    frames = raw_data[i:i+CHUNK]
    stream.write(frames)
    wf.writeframes(frames)

# 스트림 및 파일 종료
stream.stop_stream()
stream.close()
wf.close()

# PyAudio 종료
p.terminate()
