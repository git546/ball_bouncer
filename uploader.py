from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# OAuth 2.0 인증을 위한 스코프 설정
SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate():
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', scopes=['https://www.googleapis.com/auth/youtube.upload'])
    credentials = flow.run_local_server(port=0)
    return build('youtube', 'v3', credentials=credentials)

def upload_short(youtube, file_path, title, description, category_id, keywords):
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
    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=media
    )

    response = request.execute()
    print(f'Uploaded Shorts video with ID: {response["id"]}')

if __name__ == '__main__':
    youtube = authenticate()
    upload_short(youtube, 'final_output.mp4', 'My YouTube Short', 'This is a short video.', '22', 'funny, short video')
 