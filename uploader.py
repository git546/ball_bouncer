import os
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

def authenticate(client_secret_files):
    for client_secrets_file in client_secret_files:
        try:
            flow = InstalledAppFlow.from_client_secrets_file(
                client_secrets_file, scopes=['https://www.googleapis.com/auth/youtube.upload'])
            credentials = flow.run_local_server(port=0)
            print(f"Using credentials from {client_secrets_file}")
            return build('youtube', 'v3', credentials=credentials)
        except Exception as e:
            print(f"Failed to authenticate using {client_secrets_file}: {e}")
    raise Exception("All client secrets exhausted.")

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
            return None
        else:
            raise

if __name__ == '__main__':
    client_secret_files = [
        'client_secrets.json'
        'client_secrets.json',
        'client_secrets_2.json',
        'client_secrets_3.json'
    ]
    youtube = authenticate(client_secret_files)
    upload_video(youtube, 'final_output.mp4', 'My YouTube Short', 'This is a short video.', '22', 'funny, short video')
