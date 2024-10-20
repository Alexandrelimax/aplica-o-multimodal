from fastapi import APIRouter, HTTPException, Depends
from fastapi.responses import JSONResponse
from services.prompt_service import PromptService
from security.user_provider import get_authenticated_user

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

    async def load_prompts(self, user=Depends(get_authenticated_user)) -> JSONResponse:
        try:
            prompts = self.prompt_service.get_loaded_prompts(user.email)
            return JSONResponse(content={"prompts": prompts})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def save_prompt(self, prompt: str, project_name: str, context_filename: str, user_email=Depends(get_authenticated_user)) -> JSONResponse:
        try:
            self.prompt_service.save_loaded_prompts(user_email, prompt, project_name, context_filename)
            return JSONResponse(content={"status": "Prompt saved"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def delete_prompt(self, prompt_id: int, user_email=Depends(get_authenticated_user)) -> JSONResponse:
        try:
            self.prompt_service.delete_prompt(user_email, prompt_id)
            return JSONResponse(content={"status": "Prompt deleted"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    async def reset_prompts(self, user_email=Depends(get_authenticated_user)) -> JSONResponse:
        try:
            self.prompt_service.reset_prompts(user_email)
            return JSONResponse(content={"status": "Prompts reset"})
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
