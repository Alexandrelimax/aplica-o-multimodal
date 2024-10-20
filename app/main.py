from fastapi import FastAPI
from controllers.content_controller import ContentController
from controllers.prompt_controller import PromptController

from services.generation_service import GenerationService
from services.prompt_service import PromptService
from handlers.file_handler import FileHandler

from repositories.storage_repository import StorageRepository
from repositories.context_repository import ContextRepository

from cache.redis_cache import RedisCacheClient


app = FastAPI()

# Configura o Redis (Memory Store) e o contexto do repositório
redis_cache = RedisCacheClient(host="your-redis-host", port=6379, db=0)

# Instancia os repositórios
storage_repository = StorageRepository(bucket_name="your-bucket-name")
context_repository = ContextRepository(bucket_name="your-bucket-name")

# Instancia os serviços
file_handler = FileHandler()
generation_service = GenerationService(storage_repository, file_handler)
prompt_service = PromptService(cache_client=redis_cache, context_repository=context_repository)

# Instancia os controladores
content_controller = ContentController(generation_service)
prompt_controller = PromptController(prompt_service)

# Inclui os routers dos controladores no FastAPI
app.include_router(content_controller.router)
app.include_router(prompt_controller.router)



@app.get("/")
def read_root():
    return {"message": "API is running"}

