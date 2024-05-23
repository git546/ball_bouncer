from pydub import AudioSegment
import numpy as np
import librosa
import os

# ffmpeg 환경 설정
ffmpeg_path = r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin'  # 실제 ffmpeg 설치 경로로 변경하세요.
if ffmpeg_path not in os.environ['PATH']:
    os.environ['PATH'] += os.pathsep + ffmpeg_path

def rms_to_db(rms):
    """RMS 값을 dB로 변환합니다."""
    return 20 * np.log10(rms + 1e-6)  # 1e-6은 로그 0 방지를 위한 작은 값입니다.

def detect_impacts(audio_segment, threshold_db=-20, chunk_length_ms=1000):
    """
    오디오 파일에서 충돌로 추정되는 부분을 감지합니다.

    Args:
    - audio_segment (AudioSegment): 분석할 오디오 세그먼트
    - threshold_db (float): 볼륨 변화의 임계값 (dB)
    - chunk_length_ms (int): 분할할 오디오 조각의 길이 (밀리초 단위)

    Returns:
    - List[AudioSegment]: 감지된 충돌 부분의 오디오 세그먼트 리스트
    """
    samples = np.array(audio_segment.get_array_of_samples())
    samples = samples.astype(np.float32)
    samples /= np.iinfo(audio_segment.array_type).max

    # Librosa를 사용하여 오디오 신호의 RMS 에너지를 계산합니다.
    rms = librosa.feature.rms(y=samples, frame_length=2048, hop_length=512)[0]

    # RMS 값을 dB로 변환합니다.
    rms_db = rms_to_db(rms)

    # 볼륨 변화가 임계값을 초과하는 지점을 찾습니다.
    impacts = np.where(np.diff(rms_db) > threshold_db)[0]

    impact_segments = []
    for impact in impacts:
        start_ms = int((impact * 512) / audio_segment.frame_rate * 1000)
        end_ms = start_ms + chunk_length_ms
        if end_ms <= len(audio_segment):
            impact_segment = audio_segment[start_ms:end_ms]
            impact_segments.append((impact_segment, rms_db[impact]))

    # RMS 에너지가 가장 큰 상위 10개 충돌 선택
    impact_segments = sorted(impact_segments, key=lambda x: x[1], reverse=True)[:10]
    return [segment for segment, rms_value in impact_segments]

def split_audio(input_path, output_dir, chunk_length_ms=1000, threshold_db=-20):
    """
    긴 오디오 파일을 여러 개의 짧은 오디오 파일로 분할합니다.

    Args:
    - input_path (str): 입력 오디오 파일 경로
    - output_dir (str): 출력 디렉토리 경로
    - chunk_length_ms (int): 분할할 오디오 조각의 길이 (밀리초 단위)
    - threshold_db (float): 볼륨 변화의 임계값 (dB)
    """
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    audio = AudioSegment.from_file(input_path)
    impact_segments = detect_impacts(audio, threshold_db, chunk_length_ms)

    for i, segment in enumerate(impact_segments):
        try:
            chunk_name = f"{os.path.splitext(os.path.basename(input_path))[0]}_impact{i}.mp3"
            chunk_path = os.path.join(output_dir, chunk_name)
            segment.export(chunk_path, format="mp3")
            print(f"Exported {chunk_path}")
        except Exception as e:
            print(f"Error exporting segment {i} from {input_path}: {e}")

def process_directory(input_dir, output_dir, chunk_length_ms=1000, threshold_db=-20):
    """
    지정된 디렉토리 내의 모든 오디오 파일을 가공합니다.

    Args:
    - input_dir (str): 입력 오디오 파일들이 있는 디렉토리 경로
    - output_dir (str): 출력 디렉토리 경로
    - chunk_length_ms (int): 분할할 오디오 조각의 길이 (밀리초 단위)
    - threshold_db (float): 볼륨 변화의 임계값 (dB)
    """
    for filename in os.listdir(input_dir):
        input_path = os.path.join(input_dir, filename)
        if os.path.isfile(input_path):
            split_audio(input_path, output_dir, chunk_length_ms, threshold_db)

if __name__ == "__main__":
    # 긴 임팩트 사운드 파일들이 있는 디렉토리 경로
    input_directory = "effect"
    output_directory = "proceed_effect"

    # 디렉토리 내의 모든 오디오 파일을 처리
    process_directory(input_directory, output_directory, chunk_length_ms=1000, threshold_db=-10)
