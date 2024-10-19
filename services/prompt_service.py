from repositories.context_repository import ContextRepository
import json

class PromptService:
    def __init__(self, cache_client, context_repository: ContextRepository):
        self.cache_client = cache_client
        self.context_repository = context_repository
        self.is_gae_env = os.getenv('GAE_ENV', "") == "standard"
        self.global_loaded_prompts = dict()

    def get_loaded_prompts(self):
        # Carrega prompts do cache ou do Google Cloud Storage via ContextRepository
        user = get_iap_user()
        if user not in self.global_loaded_prompts:
            loaded_prompts = []
            if self.is_gae_env:
                cached_prompts = self.cache_client.get(user)
                if cached_prompts is None:
                    self.cache_client.add(user, json.dumps(loaded_prompts), 14400)
                else:
                    loaded_prompts = json.loads(cached_prompts)
            self.global_loaded_prompts[user] = loaded_prompts
        return self.global_loaded_prompts[user]

    def save_loaded_prompts(self, prompt, project_name, filename):
        # Salva prompts no cache e em um contexto via ContextRepository
        loaded_prompts = self.get_loaded_prompts()
        loaded_prompts.append((prompt, project_name, filename))
        self.global_loaded_prompts[get_iap_user()] = loaded_prompts
        self.context_repository.save_prompt_context(project_name, filename, json.dumps(loaded_prompts))

    def delete_prompt(self, prompt_id: int):
        # Remove um prompt específico
        loaded_prompts = self.get_loaded_prompts()
        if 0 <= prompt_id < len(loaded_prompts):
            del loaded_prompts[prompt_id]
        self.save_loaded_prompts(loaded_prompts)

    def reset_prompts(self):
        # Reseta os prompts no cache
        self.save_loaded_prompts([])
