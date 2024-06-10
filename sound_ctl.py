import os
import numpy as np
from pydub import AudioSegment
from music21 import stream, note, midi
from midi2audio import FluidSynth

# ffmpeg 경로 설정
FFMPEG_PATH = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'
os.environ['PATH'] += os.pathsep + FFMPEG_PATH

# pydub에 ffmpeg 경로 설정
AudioSegment.converter = os.path.join(FFMPEG_PATH, "ffmpeg")
AudioSegment.ffmpeg = os.path.join(FFMPEG_PATH, "ffmpeg")
AudioSegment.ffprobe = os.path.join(FFMPEG_PATH, "ffprobe")

# FluidSynth 설정 (사운드폰트 경로 설정 필요)
SOUNDFONT_PATH = 'FluidR3_GM.sf2'  # 사운드폰트 파일 이름만 지정 (같은 폴더에 둠)
FLUIDSYNTH_PATH = r'C:\fluidsynth-2.3.5-win10-x64\bin'  # fluidsynth.exe 경로 설정

# 환경 변수에 fluidsynth 경로 추가
os.environ['PATH'] += os.pathsep + FLUIDSYNTH_PATH

# FluidSynth 객체 생성
fs = FluidSynth(SOUNDFONT_PATH)

# 주파수를 기반으로 음 생성
def generate_tone(note_name, duration, temp_midi_path='temp_tone.mid', temp_wav_path='temp_tone.wav'):
    # Music21 스트림 생성
    s = stream.Stream()
    n = note.Note(note_name)
    n.quarterLength = duration
    s.append(n)
    
    # MIDI 파일로 저장
    mf = midi.translate.music21ObjectToMidiFile(s)
    mf.open(temp_midi_path, 'wb')
    mf.write()
    mf.close()

    # MIDI 파일을 WAV 파일로 변환
    fs.midi_to_audio(temp_midi_path, temp_wav_path)
    os.remove(temp_midi_path)  # 임시 MIDI 파일 삭제

    return temp_wav_path

# 음 데이터를 AudioSegment로 변환하는 함수
def file_to_audio_segment(file_path):
    return AudioSegment.from_wav(file_path)

# 주어진 시간에 소리를 삽입하는 함수
def add_collision_sounds(collision_times, output_path, note_duration, video_duration):
    """
    주어진 시간에 맞춰 소리를 삽입하여 무음 배경 오디오 파일을 생성하는 함수.

    Args:
    - collision_times (list[int]): 충돌이 일어나는 시간(밀리초) 리스트
    - output_path (str): 결과 오디오 파일을 저장할 경로
    - note_duration (int): 각 충돌에 삽입할 음 길이 (밀리초 단위)
    - video_duration (int): 비디오 길이 (밀리초 단위)

    Returns:
    - None
    """
    # 비디오 길이에 맞춘 무음 오디오 생성
    base_audio = AudioSegment.silent(duration=video_duration)
    temp_wav_path = 'temp_tone.wav'

    # 각 충돌 시간에 피아노 소리 삽입
    for time in collision_times:
        note_name = np.random.choice(['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4'])  # 무작위 음 선택
        generate_tone(note_name, note_duration / 1000.0, temp_midi_path='temp_tone.mid', temp_wav_path=temp_wav_path)
        
        # 파일이 생성되었는지 확인
        if os.path.exists(temp_wav_path):
            instrument_tone = file_to_audio_segment(temp_wav_path)
            base_audio = base_audio.overlay(instrument_tone, position=time)
            os.remove(temp_wav_path)  # 임시 파일 삭제
        else:
            print(f"Error: File '{temp_wav_path}' was not created.")
    
    base_audio.export(output_path, format="mp3")
