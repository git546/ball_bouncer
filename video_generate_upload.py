from record_video import run_game_and_create_audio, merge_audio_video
from uploader import authenticate, upload_video

import sys
import os
sys.path.append(os.path.join(os.path.dirname(sys.executable), "cv2"))

import cv2
import numpy as np
import pydub
import music21
import midi2audio
import random
import subprocess
import ball_bounce
import sound_ctl
import game_configurations

def main():
    # run_game_and_create_audio 함수가 문자열 제목과 비디오 길이를 반환하도록 수정되었습니다.
    Video_Title, video_duration = run_game_and_create_audio()
    
    # 디버깅 로그 추가: Video_Title과 video_duration을 출력하여 확인
    print(f"Generated Video Title: {Video_Title}")
    print(f"Video Duration: {video_duration} seconds")
    
    # Video_Title이 문자열로 보장되도록 str()로 변환
    Video_Title = str(Video_Title)
    
    merge_audio_video(video_filename='game_video.avi', audio_filename='game_audio.mp3', output_filename='final_output.mp4', video_duration=video_duration)
    
    youtube = authenticate([r'C:\Users\SCHOOL\Desktop\ball_bouncer\client_secrets.json'])
    upload_video(youtube, 'final_output.mp4', Video_Title, '', '22', 'graphics, sound, computer_work')

if __name__ == "__main__":
    main()
