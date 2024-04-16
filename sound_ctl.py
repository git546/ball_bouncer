from pydub import AudioSegment
import os

ffmpeg_path = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'  # 여기서 경로는 실제 ffmpeg 설치 경로로 변경해야 합니다.
os.environ['PATH'] += os.pathsep + ffmpeg_path

def add_collision_sounds_based_on_type(collision_times, collision_sound_path, output_path, audio_type, clip_length_ms=2500):
    """
    주어진 시간에 맞춰 뮤직 또는 효과음을 삽입하여 무음 배경 오디오 파일을 생성하는 함수.

    Args:
    - collision_times (list[int]): 충돌이 일어나는 시간(밀리초) 리스트
    - collision_sound_path (str): 충돌 시 재생할 오디오 파일 경로
    - output_path (str): 결과 오디오 파일을 저장할 경로
    - audio_type (str): 'music' 또는 'effect'를 지정하여 오디오 타입 선택
    - clip_length_ms (int): 각 충돌에 삽입할 오디오 길이 (밀리초 단위, 'music' 타입에서만 필요)

    Returns:
    - None
    """
    # 충돌 소리 파일 로드
    collision_sound = AudioSegment.from_file(collision_sound_path).apply_gain(60)

    # 1분 길이의 무음 오디오 생성
    base_audio = AudioSegment.silent(duration=60000)  # 1분 = 60000 밀리초
    if audio_type == 'music':
        # 각 충돌 시간에 해당하는 연속된 노래 부분을 잘라서 삽입 ('music')
        total_length = len(collision_sound)
        for index, time in enumerate(collision_times):
            start_clip = index * clip_length_ms
            end_clip = start_clip + clip_length_ms
            if end_clip > total_length:
                end_clip = total_length
            clip = collision_sound[start_clip:end_clip]
            base_audio = base_audio.overlay(clip, position=time)
            
    elif audio_type == 'effect':
        # 각 충돌 시간에 동일한 효과음 삽입 ('effect')
        for time in collision_times:
            base_audio = base_audio.overlay(collision_sound, position=time)

    # 결과 오디오 파일 저장
    base_audio.export(output_path, format="mp3")

"""
# 함수 호출 예시
# 'music' 타입으로 노래의 특정 부분을 5초, 15초, 20초 지점에 삽입
add_collision_sounds_based_on_type([5000, 15000, 20000], "Queencards.mp3", "game_audio.mp3", 'music', 2500)
"""