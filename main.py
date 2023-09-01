import os
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload


# Autenticación OAuth 2.0
def get_authenticated_service():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()
    return build(API_SERVICE_NAME, API_VERSION, credentials=credentials)


# Subir video
def initialize_upload(youtube, filename):
    media_body = MediaFileUpload(filename, chunksize=-1, resumable=True, mimetype='video/mp4')
    body = {
        'snippet': {
            'title': 'Mi video de prueba',
            'description': 'Este es un video de prueba',
            'tags': ['test', 'ejemplo'],
            'categoryId': '22'
        },
        'status': {
            'privacyStatus': 'private'  # o 'public' o 'unlisted'
        }
    }

    request = youtube.videos().insert(
        part=','.join(body.keys()),
        body=body,
        media_body=media_body
    )

    response = None
    while response is None:
        status, response = request.next_chunk()

    print(f"Subido video con ID: {response['id']}")

if __name__ == '__main__':
    CLIENT_SECRETS_FILE = 'credentials.json'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
    API_SERVICE_NAME = 'youtube'
    API_VERSION = 'v3'
    
    youtube = get_authenticated_service()
    try:
        initialize_upload(youtube, 'ruta_del_video.mp4')  # Reemplaza con la ruta de tu video
    except HttpError as e:
        print(f"Ocurrió un error HTTP: {e.resp.status} - {e.content}")
