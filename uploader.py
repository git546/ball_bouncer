import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.transport.requests import Request

# YouTube API를 사용하기 위한 스코프 지정
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate(client_secret_files, token_file='token.pkl'):
    # 저장된 크레덴셜을 불러와서 유효한지 확인
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

        # 크레덴셜이 만료되었는지 확인하고 필요시 리프레시
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
    else:
        # 크레덴셜이 없거나 유효하지 않은 경우 새로 인증
        for client_secrets_file in client_secret_files:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(
                    client_secrets_file, scopes=SCOPES)
                credentials = flow.run_local_server(port=0)
                print(f"Using credentials from {client_secrets_file}")
                
                # 인증된 크레덴셜을 파일에 저장
                with open(token_file, 'wb') as token:
                    pickle.dump(credentials, token)
                
                return build('youtube', 'v3', credentials=credentials)
            except Exception as e:
                print(f"Failed to authenticate using {client_secrets_file}: {e}")
        raise Exception("All client secrets exhausted.")
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file_path, title, description, category_id, keywords):
    # 비디오 업로드에 필요한 메타데이터 설정
    body = {
        'snippet': {
            'title': title,
            'description': description + "\n#Shorts",
            'tags': keywords.split(',') + ['Shorts'],
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': 'public'
        }
    }

    # 파일 업로드 준비
    media = MediaFileUpload(file_path, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        # YouTube에 비디오 업로드 요청 실행
        response = request.execute()
        print(f'Uploaded video with ID: {response["id"]}')
    except HttpError as error:
        # API 사용량 초과 등의 HTTP 에러 처리
        if error.resp.status in [403, 429]:
            print("Quota exceeded error caught. Exiting...")
            return None
        else:
            # 기타 예상치 못한 HTTP 에러 발생 시 예외를 다시 발생시키기
            raise

if __name__ == '__main__':
    # 클라이언트 비밀 파일 리스트
    client_secret_files = [
        'client_secrets.json'
    ]
    # YouTube API 인증 수행
    youtube = authenticate(client_secret_files)
    # 비디오 파일 업로드 수행
    upload_video(youtube, 'final_output.mp4', 'My YouTube Short', 'This is a short video.', '22', 'funny, short video')
