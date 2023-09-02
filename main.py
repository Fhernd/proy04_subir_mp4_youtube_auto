import os
import sys
import time

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler


class SubidaAutomaticaYouTube(FileSystemEventHandler):
    """
    Clase que gestiona los eventos de subida automática a YouTube.
    """
    def __init__(self):
        """
        Constructor de la clase.
        """
        self.CLIENT_SECRETS_FILE = 'credentials.json'
        self.SCOPES = ['https://www.googleapis.com/auth/youtube.upload']
        self.API_SERVICE_NAME = 'youtube'
        self.API_VERSION = 'v3'
        
        self.youtube = self.get_authenticated_service()
    
    """
    Clase que gestiona los eventos de renombrado de archivos.
    """
    def on_created(self, event):
        """
        Método que se ejecuta cuando se modifica un archivo.
        
        Args:
            event (FileSystemEvent): Evento de modificación de archivo.
        """
        if event.is_directory:
            return
        
        print('Archivo creado: %s' % event.src_path)

        extension = os.path.splitext(event.src_path)[1]

        if extension != '.mp4':
            print('No es un archivo de video')
            return

        try:
            self.initialize_upload(self.youtube, event.src_path)  # Reemplaza con la ruta de tu video
        except HttpError as e:
            print(f"Ocurrió un error HTTP: {e.resp.status} - {e.content}")

    
    def get_authenticated_service(self):
        """
        Obtiene un recurso de YouTube autenticado.

        Returns:
            googleapiclient.discovery.Resource: Recurso de YouTube autenticado.
        """
        flow = InstalledAppFlow.from_client_secrets_file(self.CLIENT_SECRETS_FILE, self.SCOPES)
        credentials = flow.run_local_server()
        return build(self.API_SERVICE_NAME, self.API_VERSION, credentials=credentials)


    def initialize_upload(self, youtube, filename):
        """
        Sube un video a YouTube.

        Args:
            youtube (googleapiclient.discovery.Resource): Recurso de YouTube.
            filename (str): Ruta del archivo a subir.
        """
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


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else '.'
    
    event_handler = SubidaAutomaticaYouTube()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
