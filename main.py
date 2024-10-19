from fastapi import FastAPI
from controllers.content_controller import ContentController
from controllers.prompt_controller import PromptController

from services.generation_service import GenerationService
from services.prompt_service import PromptService
from handlers.file_handler import FileHandler

from repositories.storage_repository import StorageRepository

app = FastAPI()

# Instancia os repositórios
storage_repository = StorageRepository(bucket_name="your-bucket-name")

# Instancia os serviços
local_file_service = FileHandler()
generation_service = GenerationService(storage_repository, local_file_service)
prompt_service = PromptService()

# Instancia os controladores e associa os serviços necessários
content_controller = ContentController(generation_service)
prompt_controller = PromptController(prompt_service)

# Inclui os routers dos controladores no FastAPI
app.include_router(content_controller.router)
app.include_router(prompt_controller.router)


# Rota principal para verificação
@app.get("/")
def read_root():
    return {"message": "Teste API"}
