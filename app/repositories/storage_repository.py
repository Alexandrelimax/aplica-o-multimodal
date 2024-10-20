# app/repositories/storage_repository.py
from google.cloud import storage
from config.settings import MEDIA_SUPPORTED_TYPES, PROG_LANGUAGES, TXT_FILES


class StorageRepository:
    def __init__(self, bucket_name: str):
        self.client = storage.Client()
        self.bucket = self.client.bucket(bucket_name)


    async def upload_blob(self, user_email: str, project_name: str, file: bytes, filename: str) -> str:
        #Faz o upload de um arquivo (blob) para o bucket, organizando-o dentro da pasta do usuário/projeto.
        blob_path = f"{user_email}/{project_name}/{filename}"
        blob = self.bucket.blob(blob_path)
        blob.upload_from_string(file)
        return f"File {filename} uploaded successfully at {blob_path}"


    async def get_code_midia_blobs(self, user_email: str, project_name: str, include_txt_midia: bool):
        #Recupera os blobs de código ou mídia de texto para análise, dependendo do tipo de conteúdo permitido.
        folder = f"{user_email}/{project_name}"
        valid_extensions = PROG_LANGUAGES + (TXT_FILES if include_txt_midia else [])
        
        # Recupera blobs filtrando por extensão e tipos de mídia
        blobs = await self.get_blobs(folder, valid_extensions, MEDIA_SUPPORTED_TYPES)
        
        if include_txt_midia:
            return [blob for blob in blobs 
                    if self._is_valid_extension(blob.name, valid_extensions) 
                    or blob.content_type in MEDIA_SUPPORTED_TYPES]
        
        return [blob for blob in blobs if self._is_valid_extension(blob.name, PROG_LANGUAGES)]


    async def get_blobs(self, folder: str, file_types_array: list, blob_types: list = []):
        #Recupera blobs de um determinado prefixo (pasta) no bucket, filtrando por tipos de arquivo e tipos MIME suportados.
        blobs = self.bucket.list_blobs(prefix=folder)
        blobs_to_analyze = []
        
        for blob in blobs:
            if blob.size > 5:  # Exclui arquivos muito pequenos (provavelmente inválidos)
                if self._is_valid_extension(blob.name, file_types_array) or blob.content_type in blob_types:
                    blobs_to_analyze.append(blob)
        
        return blobs_to_analyze


    def _is_valid_extension(self, filename: str, valid_extensions: list) -> bool:
        #Verifica se a extensão do arquivo é válida (suportada).
        ext = filename.split(".")[-1].lower()
        return ext in valid_extensions
