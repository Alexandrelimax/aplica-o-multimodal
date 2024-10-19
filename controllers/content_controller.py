from fastapi import APIRouter, HTTPException, UploadFile, File, Depends
from fastapi.responses import JSONResponse
from services.generation_service import GenerationService
from handlers.file_handler import FileHandler
from security.user_provider import get_authenticated_user


class ContentController:
    def __init__(self, generation_service: GenerationService, file_handler: FileHandler):
        self.router = APIRouter(prefix="/content")
        self.generation_service = generation_service
        self.file_handler = file_handler
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/generate-code-analysis", self.generate_code_analysis, methods=["POST"])
        self.router.add_api_route("/upload-context", self.upload_context, methods=["POST"])
        self.router.add_api_route("/generate-unit-tests", self.generate_unit_tests, methods=["POST"])


    async def generate_code_analysis(self, project_name: str, model_name: str, include_txt_midia: bool = True, user_email: str = Depends(get_authenticated_user)) -> JSONResponse:
        try:
            # Gera a análise de código para o projeto do usuário autenticado
            result = await self.generation_service.generate_code_analysis(user_email, project_name, model_name, include_txt_midia)
            return JSONResponse(content={"status": "success", "result": result})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    async def generate_unit_tests(self, project_name: str, model_name: str, user_email: str = Depends(get_authenticated_user)) -> JSONResponse:
        try:
            # Gera os testes unitários para o projeto do usuário autenticado
            result = await self.generation_service.generate_unit_tests(user_email, project_name, model_name)
            return JSONResponse(content={"status": "success", "result": result})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))


    async def upload_context(self, project_name: str, file: UploadFile = File(...), user_email: str = Depends(get_authenticated_user)) -> JSONResponse:
        try:
            # Faz o upload do arquivo de contexto para o projeto do usuário autenticado
            url = await self.file_handler.upload_context_file(user_email, project_name, file)
            return JSONResponse(content={"status": "success", "url": url})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
