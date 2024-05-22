import cv2
import os
import random
import subprocess
from ball_bounce import Game
from sound_ctl import add_collision_sounds_based_on_type
from game_configurations import colors

# Constants for paths and filenames can be set here or read from environment/config
FFMPEG_PATH = os.environ.get('FFMPEG_PATH', r'C:\ffmpeg-2024-04-10-git-0e4dfa4709-full_build\bin')
os.environ['PATH'] += os.pathsep + FFMPEG_PATH

def select_random_file(folder):
    """Given a folder, returns the path of a random file from that folder."""
    files = [f for f in os.listdir(folder) if os.path.isfile(os.path.join(folder, f))]
    if files:
        return os.path.join(folder, random.choice(files))
    return None

def get_video_duration(filename):
    """ Return the duration of a video in seconds """
    video = cv2.VideoCapture(filename)
    if not video.isOpened():
        return None
    fps = video.get(cv2.CAP_PROP_FPS)
    frame_count = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    duration = frame_count / fps
    video.release()
    return duration

def get_video_framerate(filename):
    """ Return the frame rate of a video """
    result = subprocess.run(
        ["ffprobe", "-v", "error", "-select_streams", "v:0", "-show_entries", "stream=r_frame_rate", "-of", "csv=p=0", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
    )
    framerate = result.stdout.decode('utf-8').strip()
    num, denom = map(int, framerate.split('/'))
    return num / denom

def convert_collision_frames_to_times(collision_frames, framerate):
    """ Convert collision frames to milliseconds with precise floating-point division """
    collision_times = [round(frame * 1000 / framerate) for frame in collision_frames]
    print(f"Converted collision frames to times (ms): {collision_times}")
    return collision_times


def trim_video(input_filename, output_filename, video_duration):
    """ Trim the video file to keep the last 60 seconds """
    start_time = max(0, video_duration - 60)  # Ensure start_time is not negative
    command = [
        'ffmpeg', '-i', input_filename,
        '-ss', str(start_time), '-t', '60',  # '-t' specifies the duration to keep
        '-c', 'copy', output_filename
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def adjust_collision_times(collision_times, cut_time):
    """ Adjust collision times based on the trimmed video start time """
    adjusted_times = [time - cut_time for time in collision_times if time > cut_time]
    return adjusted_times

def generate_video_title(game, audio_type):
    # 게임 설정에서 볼과 테두리의 색상을 확인
    ball_color_name = '\b'
    
    for color_name, color_value in colors.items():
        if color_value == game.ball.color:
            ball_color_name = color_name
            break
    
    if game.rainbow_checker:
        ball_color_name = 'rainbow'
    
    # 볼의 색상을 제목에 포함
    title_parts = [f"This {ball_color_name.capitalize()} Ball"]

    # 설정에 따라 "Getting Bigger" 또는 "Getting Smaller" 추가
    if game.ball.growth > 1:
        title_parts.append("Getting Bigger")
    elif game.ball.growth < 1:
        title_parts.append("Getting Smaller")

    # 사운드 설정에 따라 제목 변경
    title_parts.append("with")
    title_parts.append(audio_type)

    # 제목 부분을 연결
    return " ".join(title_parts)

def run_game_and_create_audio(video_filename='game_video.avi', output_audio='game_audio.mp3',
                              clip_length_ms=1000, target_duration=75):
    
    audio_type = random.choice(['music', 'effect'])
    
    while True:
        print("Starting game...")
        game = Game()
        game.run()
        print("Game ended.")

        video_duration = get_video_duration(video_filename)
        framerate = get_video_framerate(video_filename)
        print(f"Video duration: {video_duration:.2f} seconds")
        print(f"Video framerate: {framerate:.2f} fps")
        
        if video_duration > target_duration:
            print("Video is too long,  restarting...")
            continue
        break

    collision_frames = getattr(game, 'collision_recorder', None).get_collision_frames() if game else []
    
    if collision_frames:
        print(f"Collision frames recorded: {collision_frames}")
        collision_times = convert_collision_frames_to_times(collision_frames, framerate)
        adjusted_collision_times = adjust_collision_times(collision_times, max(0, video_duration - 60) * 1000)
        print(f"Adjusted collision times: {adjusted_collision_times}")
        
        folder = 'music' if audio_type == 'music' else 'effect'
        collision_sound_path = select_random_file(folder)
        if collision_sound_path:
            add_collision_sounds_based_on_type(adjusted_collision_times, collision_sound_path, output_audio, audio_type, clip_length_ms, video_duration * 1000)
            print(f"Audio file created: {output_audio}")
        else:
            print("No audio file found in the specified folder.")
    else:
        print("No collision times recorded.")
        
    Video_Title = generate_video_title(game, audio_type)
    return Video_Title, video_duration

def merge_audio_video(audio_filename='game_audio.mp3', video_filename='game_video.avi', output_filename='final_output.mp4', video_duration=0):
    command = [
        'ffmpeg',
        '-y',
        '-i', video_filename,
        '-i', audio_filename,
        '-c:v', 'libx264',  # H.264 코덱 사용
        '-crf', '0',  # 품질을 0으로 설정 (무손실)
        '-preset', 'slow',  # 인코딩 속도와 압축 효율 사이의 균형 설정, 더 좋은 압축을 위해 slow 사용
        '-c:a', 'aac',  # 오디오 코덱 AAC
        '-strict', 'experimental',
        '-b:a', '192k',  # 오디오 비트레이트를 192 kbps로 설정
        output_filename
    ]
    try:
        process = subprocess.run(command, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        print("Merge completed successfully.")
        print("STDOUT:", process.stdout)
    except subprocess.CalledProcessError as e:
        print("An error occurred while merging:")
        print("Return code:", e.returncode)
        print("Output:", e.output)
        print("Error output:", e.stderr)

    # 최종 출력 트리밍 (최종 결과물의 길이가 60초를 초과하는 경우에만)
    if video_duration > 60:
        print("Trimming final output to keep the last 60 seconds...")
        trim_video(output_filename, output_filename, video_duration)

def main():
    Video_Title, video_duration = run_game_and_create_audio()
    merge_audio_video(video_filename='game_video.avi', audio_filename='game_audio.mp3', output_filename='final_output.mp4', video_duration=video_duration)
    print(Video_Title)

if __name__ == "__main__":
    main()
