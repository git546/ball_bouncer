from pydub import AudioSegment
import os

# ffmpeg 환경 설정
ffmpeg_path = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'  # 실제 ffmpeg 설치 경로로 변경하세요.
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
    collision_sound = AudioSegment.from_file(collision_sound_path).apply_gain(20)

    # 1분 길이의 무음 오디오 생성
    base_audio = AudioSegment.silent(duration=59000)  # 약 1분 = 59000 밀리초

    if audio_type == 'music':
        # 충돌 시간 병합을 위한 처리
        collision_times.sort()
        merged_times = []
        current_start = collision_times[0]
        current_end = current_start + clip_length_ms

        for time in collision_times[1:]:
            if time <= current_end:  # 현재 시간이 이전 시간과 겹치면 병합
                current_end = max(current_end, time + clip_length_ms)
            else:
                merged_times.append((current_start, current_end))
                current_start = time
                current_end = time + clip_length_ms
        merged_times.append((current_start, current_end))  # 마지막 구간 추가

        # 병합된 시간에 따라 오디오 삽입
        for start, end in merged_times:
            duration = end - start
            clip = collision_sound[:duration]
            base_audio = base_audio.overlay(clip, position=start)

    elif audio_type == 'effect':
        # 각 충돌 시간에 동일한 효과음 동시 재생
        for time in collision_times:
            base_audio = base_audio.overlay(collision_sound, position=time)

    # 결과 오디오 파일 저장
    base_audio.export(output_path, format="mp3")