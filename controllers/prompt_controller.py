from fastapi import APIRouter, HTTPException
from services.prompt_service import PromptService
from fastapi.responses import JSONResponse

class PromptController:
    def __init__(self, prompt_service: PromptService):
        self.router = APIRouter(prefix="/prompts")
        self.prompt_service = prompt_service
        self.register_routes()

    def register_routes(self):
        self.router.add_api_route("/load", self.load_prompts, methods=["GET"])
        self.router.add_api_route("/save", self.save_prompt, methods=["POST"])
        self.router.add_api_route("/delete", self.delete_prompt, methods=["DELETE"])
        self.router.add_api_route("/reset", self.reset_prompts, methods=["POST"])

    async def load_prompts(self) -> JSONResponse:
        try:
            # Carregando prompts via PromptService
            prompts = self.prompt_service.get_loaded_prompts()
            return JSONResponse(content={"prompts": prompts})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def save_prompt(self, prompt: str, project_name: str, context_filename: str) -> JSONResponse:
        try:
            # Salva os prompts no PromptService
            self.prompt_service.save_loaded_prompts(prompt, project_name, context_filename)
            return JSONResponse(content={"status": "Prompt saved"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_prompt(self, prompt_id: int) -> JSONResponse:
        try:
            # Deleta o prompt via PromptService
            self.prompt_service.delete_prompt(prompt_id)
            return JSONResponse(content={"status": "Prompt deleted"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def reset_prompts(self) -> JSONResponse:
        try:
            self.prompt_service.reset_prompts()
            return JSONResponse(content={"status": "Prompts reset"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
