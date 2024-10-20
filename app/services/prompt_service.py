import json
from repositories.context_repository import ContextRepository
from cache.redis_cache import RedisCacheClient

class PromptService:
    def __init__(self, cache_client: RedisCacheClient, context_repository: ContextRepository):
        self.cache_client = cache_client
        self.context_repository = context_repository

    def get_loaded_prompts(self, user_email: str):
        cached_prompts = self.cache_client.get(user_email)
        if cached_prompts is None:
            loaded_prompts = self.context_repository.load_prompt_context(user_email)
            self.cache_client.add(user_email, loaded_prompts)  # Cacheia os prompts
            return loaded_prompts
        return cached_prompts

    def save_loaded_prompts(self, user_email: str, prompt: str, project_name: str, filename: str):
        loaded_prompts = self.get_loaded_prompts(user_email)
        loaded_prompts.append((prompt, project_name, filename))
        
        self.cache_client.add(user_email, loaded_prompts)
        self.context_repository.save_prompt_context(user_email, project_name, filename, json.dumps(loaded_prompts))

    def delete_prompt(self, user_email: str, prompt_id: int):
        loaded_prompts = self.get_loaded_prompts(user_email)
        if 0 <= prompt_id < len(loaded_prompts):
            del loaded_prompts[prompt_id]
            self.cache_client.add(user_email, loaded_prompts)

            # Opcional: Atualizar também no ContextRepository se necessário
            self.context_repository.save_prompt_context(user_email, "", "", json.dumps(loaded_prompts))

    def reset_prompts(self, user_email: str):
        # Limpa os prompts no Redis e no contexto
        self.cache_client.add(user_email, [])  # Zera os prompts no cache
        self.context_repository.reset_prompt_context(user_email)
