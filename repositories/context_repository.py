from google.cloud import storage
import json

class ContextRepository:
    def __init__(self, bucket_name: str):
        self.storage_client = storage.Client()
        self.bucket = self.storage_client.bucket(bucket_name)

    def save_prompt_context(self, user_email: str, project_name: str, filename: str, data: str):
        # Salva o contexto do prompt no bucket, organizado por usuário e projeto
        if not project_name or not filename:
            return
        blob_path = f"{user_email}/{project_name}/{filename}.json"
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(data, content_type='application/json')
        print(f"Context saved at: {blob_path}")

    def load_prompt_context(self, user_email: str, project_name: str, filename: str):
        # Carrega o contexto do prompt do bucket
        blob_path = f"{user_email}/{project_name}/{filename}.json"
        blob = self.bucket.blob(blob_path)
        if blob.exists():
            data = blob.download_as_text()
            return json.loads(data)
        else:
            print(f"Context {blob_path} not found")
            return None

    def delete_prompt_context(self, user_email: str, project_name: str, filename: str):
        # Remove o contexto do prompt do bucket
        blob_path = f"{user_email}/{project_name}/{filename}.json"
        blob = self.bucket.blob(blob_path)
        if blob.exists():
            blob.delete()
            print(f"Context {blob_path} deleted.")
        else:
            print(f"Context {blob_path} not found.")
