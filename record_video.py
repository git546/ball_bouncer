import cv2
import os
import random
import subprocess
from ball_bounce import Game
from sound_ctl import add_collision_sounds_based_on_type

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

def trim_video(input_filename, output_filename, start_time, end_time):
    """ Trim the video file to the desired duration """
    command = [
        'ffmpeg', '-i', input_filename,
        '-ss', str(start_time), '-to', str(end_time),
        '-c', 'copy', output_filename
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def run_game_and_create_audio(video_filename='game_video.avi', output_audio='game_audio.mp3',
                              audio_type='music', clip_length_ms=1000, target_duration=75):
    while True:
        print("Starting game...")
        game = Game()
        game.run()
        print("Game ended.")

        video_duration = get_video_duration(video_filename)
        print(f"Video duration: {video_duration:.2f} seconds")
        
        if video_duration > target_duration:
            print("Video is too long, restarting...")
            continue
        elif video_duration < target_duration:
            break

    collision_times = getattr(game, 'collision_recorder', None).get_collision_times() if game else []
    if collision_times:
        print(f"Collision times recorded: {collision_times}")
        folder = 'music' if audio_type == 'music' else 'effect'
        collision_sound_path = select_random_file(folder)
        if collision_sound_path:
            clip_length_ms = 00#사운드 길이
            add_collision_sounds_based_on_type(collision_times, collision_sound_path, output_audio, audio_type, clip_length_ms, video_duration*1000)
            print(f"Audio file created: {output_audio}")
        else:
            print("No audio file found in the specified folder.")
    else:
        print("No collision times recorded.")

def merge_audio_video(audio_filename='game_audio.mp3', video_filename='game_video.avi', output_filename='final_output.mp4'):
    command = [
        'ffmpeg',
        '-y',
        '-i', video_filename,
        '-i', audio_filename,
        '-c:v', 'libx264',  # H.264 코덱 사용
        '-crf', '0',  # 품질을 18로 설정, 0이 최고 (무손실)이고 51이 최저 품질
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

def main():
    run_game_and_create_audio()
    merge_audio_video()

if __name__ == "__main__":
    main()