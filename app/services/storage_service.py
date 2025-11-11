from minio import Minio
from minio.error import S3Error
from app.core.config import settings
import time

class StorageService:
    def __init__(self):
        self.client = Minio(
            settings.minio_endpoint,
            access_key=settings.minio_access_key,
            secret_key=settings.minio_secret_key,
            secure=False
        )
    
    def ensure_bucket_exists(self):
        max_retries = 5
        for i in range(max_retries):
            try:
                if not self.client.bucket_exists(settings.minio_bucket):
                    self.client.make_bucket(settings.minio_bucket)
                    print(f"✅ Bucket '{settings.minio_bucket}' created")
                else:
                    print(f"✅ Bucket '{settings.minio_bucket}' already exists")
                return
            except Exception as e:
                if i < max_retries - 1:
                    print(f"⏳ Waiting for MinIO... ({i+1}/{max_retries})")
                    time.sleep(2)
                else:
                    print(f"❌ Failed to create bucket: {e}")
    
    def upload_file(self, file_data: bytes, file_name: str, path: str):
        from io import BytesIO
        import mimetypes
        object_name = f"{path.strip('/')}/{file_name}"
        content_type = mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        try:
            self.client.put_object(
                settings.minio_bucket,
                object_name,
                BytesIO(file_data),
                length=len(file_data),
                content_type=content_type
            )
            return object_name
        except S3Error as e:
            raise Exception(f"Upload failed: {e}")
    
    def get_file(self, object_name: str):
        import mimetypes
        try:
            response = self.client.get_object(settings.minio_bucket, object_name)
            content_type = mimetypes.guess_type(object_name)[0] or "application/octet-stream"
            return response, content_type
        except S3Error as e:
            raise Exception(f"File not found: {e}")

storage_service = StorageService()
