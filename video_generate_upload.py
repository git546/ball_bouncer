from record_video import run_game_and_create_audio, merge_audio_video
from uploader import authenticate, upload_video

def main():
    run_game_and_create_audio()
    merge_audio_video()
    youtube = authenticate(['client_secrets.json'])
    upload_video(youtube, 'final_output.mp4', 'My YouTube Short', 'This is a short video.', '22', 'funny, short video')

if __name__ == "__main__":
    main()