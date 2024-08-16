from google.cloud import storage
from google.cloud.storage import Client
from google.oauth2.service_account import Credentials
from io import BytesIO
import os

class GCSClient(object):
    def __init__(self, GCP_KEY_FILE) -> None:
        credentials = Credentials.from_service_account_info(GCP_KEY_FILE)
        self.client = Client(credentials=credentials, project=credentials.project_id)
    
    def upload_image(self, bucket_name, timestamp, image):
        try:
            file_name = f'image_{timestamp}.jpg'
            image_stream = BytesIO(image)

            bucket = self.client.bucket(bucket_name)
            blob = bucket.blob(file_name)
            blob.upload_from_file(image_stream, content_type='image/jpeg')
            print(f"Image uploaded to GCP bucket as {file_name}")

        except Exception as e:
            print(f"Failed to upload: {e}")