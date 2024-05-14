import os
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError
from google.auth.exceptions import RefreshError
from google.auth.transport.requests import Request

# YouTube API를 사용하기 위한 스코프 지정
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate(client_secret_files, token_file='token.pkl'):
    credentials = None
    # 저장된 크레덴셜을 불러와서 유효한지 확인
    if os.path.exists(token_file):
        with open(token_file, 'rb') as token:
            credentials = pickle.load(token)

    # 크레덴셜이 만료되었는지 확인하고 필요시 리프레시
    if credentials and credentials.expired and credentials.refresh_token:
        try:
            credentials.refresh(Request())
            # 새롭게 갱신된 토큰 저장
            with open(token_file, 'wb') as token:
                pickle.dump(credentials, token)
        except RefreshError:
            # Refresh 토큰이 유효하지 않을 때
            os.remove(token_file)
            credentials = None
            print("Refresh token is invalid, removed token file and re-authenticating.")
        except Exception as e:
            print(f"An error occurred: {e}")
            credentials = None

    # 크레덴셜이 없거나 유효하지 않은 경우 새로 인증
    if not credentials:
        for client_secrets_file in client_secret_files:
            try:
                flow = InstalledAppFlow.from_client_secrets_file(client_secrets_file, SCOPES)
                credentials = flow.run_local_server(port=0)
                # 인증된 크레덴셜을 파일에 저장
                with open(token_file, 'wb') as token:
                    pickle.dump(credentials, token)
                return build('youtube', 'v3', credentials=credentials)
            except Exception as e:
                print(f"Failed to authenticate using {client_secrets_file}: {e}")

        raise Exception("All client secrets exhausted or failed.")
    return build('youtube', 'v3', credentials=credentials)

def upload_video(youtube, file_path, title, description, category_id, keywords):
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
    media = MediaFileUpload(file_path, mimetype='video/*', resumable=True)
    request = youtube.videos().insert(part="snippet,status", body=body, media_body=media)

    try:
        response = request.execute()
        print(f'Uploaded video with ID: {response["id"]}')
    except HttpError as error:
        if error.resp.status in [403, 429]:
            print("Quota exceeded error caught. Exiting...")
        else:
            raise

if __name__ == '__main__':
    client_secret_files = ['client_secrets.json']
    youtube = authenticate(client_secret_files)
    upload_video(youtube, 'final_output.mp4', 'My YouTube Short', 'This is a short video.', '22', 'funny, short video')
