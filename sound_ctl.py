import numpy as np
from pydub import AudioSegment

# 기본 주파수(A4)
A4_FREQ = 440.0

# 특정 음의 주파수를 계산하는 함수
def note_freq(note, octave):
    return A4_FREQ * 2 ** ((note + 12 * (octave - 4) - 9) / 12)

# 주파수를 기반으로 파형 생성 함수
def generate_wave(freq, duration, sample_rate=44100, amplitude=0.5, wave_type='sine'):
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    if wave_type == 'sine':
        wave = amplitude * np.sin(2 * np.pi * freq * t)
    elif wave_type == 'triangle':
        wave = amplitude * np.arcsin(np.sin(2 * np.pi * freq * t)) * (2 / np.pi)
    elif wave_type == 'square':
        wave = amplitude * np.sign(np.sin(2 * np.pi * freq * t))
    else:
        raise ValueError("Unsupported wave type. Use 'sine', 'triangle', or 'square'.")
    return wave

# 악기 음 생성 함수
def generate_instrument_tone(note, octave, duration, sample_rate=44100, instrument='piano'):
    freq = note_freq(note, octave)
    if instrument == 'piano':
        wave = generate_wave(freq, duration, sample_rate, wave_type='sine')
    elif instrument == 'guitar':
        wave = generate_wave(freq, duration, sample_rate, wave_type='triangle')
    elif instrument == 'violin':
        wave = generate_wave(freq, duration, sample_rate, wave_type='square')
    else:
        raise ValueError("Unsupported instrument. Use 'piano', 'guitar', or 'violin'.")
    return wave

# 음 데이터를 AudioSegment로 변환하는 함수
def array_to_audio_segment(wave, sample_rate=44100):
    audio_segment = AudioSegment(
        wave.tobytes(),
        frame_rate=sample_rate,
        sample_width=wave.dtype.itemsize,
        channels=1
    )
    return audio_segment

# 주어진 충돌 시간에 악기 음을 삽입하는 함수
def add_instrument_sounds(collision_times, output_path, note_duration, video_duration, instruments):
    sample_rate = 44100
    base_audio = AudioSegment.silent(duration=video_duration)

    for time in collision_times:
        note = np.random.randint(0, 12)  # C, C#, D, D#, E, F, F#, G, G#, A, A#, B
        octave = np.random.randint(3, 6)  # 옥타브 선택
        instrument = np.random.choice(instruments)  # 무작위 악기 선택
        wave = generate_instrument_tone(note, octave, note_duration / 1000, sample_rate, instrument)
        instrument_tone = array_to_audio_segment(wave, sample_rate)
        base_audio = base_audio.overlay(instrument_tone, position=time)

    base_audio.export(output_path, format="mp3")

    return instruments

# 예제 데이터 설정
collision = [1000, 2500, 5000, 10000]  # 밀리초 단위로 충돌 시간을 지정합니다.
output_path = "output_audio.mp3"  # 출력 파일 경로
instruments = ['piano', 'guitar', 'violin']  # 사용할 악기 리스트

# 함수 호출 예제
add_instrument_sounds(collision, output_path, 2500, 15000, instruments)
