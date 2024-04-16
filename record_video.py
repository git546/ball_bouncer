from ball_bounce import Game  # ball_bounce.py에서 Game 클래스를 가져옵니다.
import subprocess

def run_game_and_merge_audio(video_filename='game_video.avi', audio_filename='game_audio.mp3', output_filename='final_output.mp4'):
    # 게임 객체 생성 및 실행
    game = Game()
    game.run()

    # 게임 종료 후 비디오 파일과 오디오 파일을 결합
    command = [
        'ffmpeg',
        '-i', video_filename,  # 비디오 입력 파일
        '-i', audio_filename,  # 오디오 입력 파일
        '-c:v', 'copy',  # 비디오 코덱은 변경하지 않음
        '-c:a', 'aac',  # 오디오 코덱은 AAC로 설정
        '-strict', 'experimental',
        output_filename  # 결과물 파일
    ]
    subprocess.run(command, check=True)

if __name__ == "__main__":
    run_game_and_merge_audio()
