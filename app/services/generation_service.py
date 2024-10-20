# app/services/generation_service.py
from vertexai.generative_models import GenerativeModel, Part
from repositories.storage_repository import StorageRepository
from handlers.file_handler import FileHandler
from config.settings import GENERATION_CONFIG, SAFETY_SETTINGS


class GenerationService:
    def __init__(self, storage_repository: StorageRepository, file_handler: FileHandler):
        self.storage_repository = storage_repository
        self.file_handler = file_handler

    async def generate_code_analysis(self, user_email: str, project_name: str, model_name: str, include_txt_midia: bool) -> str:

        model = GenerativeModel(model_name=model_name, generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS)
        
        prompt = "Analyze the following code and provide a detailed explanation."
        parts = [prompt]

        blobs_to_analyze = await self.storage_repository.get_code_midia_blobs(user_email, project_name, include_txt_midia)
        
        msg = "Files in context being considered: \n"
        for blob in blobs_to_analyze:
            uri = f"gs://{self.storage_repository.bucket.name}/{blob.name}"
            parts.append(Part.from_uri(uri=uri, mime_type=blob.content_type))
            msg += f"Added file -> {blob.name}\n"
        
        print(msg)

        response = model.generate_content(parts)
        return response.text

    async def generate_unit_tests(self, user_email: str, project_name: str, model_name: str) -> list:

        model = GenerativeModel(model_name=model_name, generation_config=GENERATION_CONFIG, safety_settings=SAFETY_SETTINGS)
        
        blobs_code_unit_test_gen = await self.storage_repository.get_code_midia_blobs(user_email, project_name, include_txt_midia=False)
        
        temp_user_folder = self.file_handler.create_temp_folder()

        unit_tests = []
        print(f"Cleaning temp_user_folder: {temp_user_folder}")

        for blob in blobs_code_unit_test_gen:
            uri = f"gs://{self.storage_repository.bucket.name}/{blob.name}"
            prompt = ["Generate unit tests for this code", Part.from_uri(uri=uri, mime_type="text/plain")]
            
            response = model.generate_content(prompt)
            
            test_filename = f"Test_{blob.name.split('/')[-1]}"
            print(f"Code: {blob.name} - Test: {test_filename}")
            
            self.file_handler.save_local_file(test_filename, response.text, temp_user_folder)
            
            unit_tests.append({
                'file_name': test_filename,
                'test_content': response.text
            })
        
        zip_filename = f"{temp_user_folder}/unit_tests.zip"
        self.file_handler.zip_folder(temp_user_folder, zip_filename)
        
        return unit_tests
