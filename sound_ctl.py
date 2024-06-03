import numpy as np
import librosa
from pydub import AudioSegment

def pitch_shift(audio_segment, n_steps):
    samples = np.array(audio_segment.get_array_of_samples())
    samples = samples.astype(np.float32)
    y_shifted = librosa.effects.pitch_shift(samples, sr=audio_segment.frame_rate, n_steps=n_steps)
    shifted_audio_segment = AudioSegment(
        y_shifted.tobytes(),
        frame_rate=audio_segment.frame_rate,
        sample_width=audio_segment.sample_width,
        channels=audio_segment.channels
    )
    return shifted_audio_segment

def add_collision_sounds_based_on_type(collision_times, collision_sound_path, output_path, audio_type, clip_length_ms, video_duration):
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
    try:
        # 충돌 소리 파일 로드
        collision_sound = AudioSegment.from_file(collision_sound_path).apply_gain(0)
    except FileNotFoundError:
        print(f"File not found: {collision_sound_path}")
        return
    except Exception as e:
        print(f"An error occurred while loading the collision sound: {e}")
        return

    # 1분 길이의 무음 오디오 생성
    base_audio = AudioSegment.silent(duration=video_duration)  # 비디오 길이에 맞춤

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
        offset = 0  # 오디오 클립에서 시작점을 계산하기 위한 오프셋
        for start, end in merged_times:
            duration = end - start
            clip = collision_sound[:duration]
            base_audio = base_audio.overlay(clip, position=start)
            offset = (offset + duration) % len(collision_sound)  # 다음 클립의 시작점을 업데이트

    elif audio_type == 'effect':
        # 각 충돌 시간에 동일한 효과음 동시 재생
        for time in collision_times:
            # 피치 변환 (높이 변경)
            n_steps = np.random.randint(-2, 3)  # -2에서 +2 사이의 무작위 피치 이동
            effect_clip = pitch_shift(collision_sound, n_steps)
            base_audio = base_audio.overlay(effect_clip, position=time)

    # 결과 오디오 파일 저장
    base_audio.export(output_path, format="mp3")

    return audio_type

# 예제 데이터 설정
collision = [1000, 2500, 5000, 10000]  # 밀리초 단위로 충돌 시간을 지정합니다.
collision_sound_path = "music/test.mp3"  # 실제 존재하는 파일 경로로 변경해야 합니다.
output_path = "output_audio.mp3"  # 출력 파일 경로
audio_type = "music"  # 오디오 타입을 'music'으로 설정

# 함수 호출 예제
# add_collision_sounds_based_on_type(collision, collision_sound_path, output_path, audio_type, 2500, 15000)
