from redis import Redis
import json

class RedisCacheClient:
    def __init__(self, host: str, port: int = 6379, db: int = 0):
        self.client = Redis(host=host, port=port, db=db)

    def get(self, key: str):
        #Busca o valor associado à chave do Redis.
        cached_value = self.client.get(key)
        if cached_value:
            return json.loads(cached_value)
        return None

    def add(self, key: str, value: dict, expiration: int = 14400):
        #Adiciona um valor ao Redis com uma chave específica e um tempo de expiração (padrão de 4 horas).
        self.client.setex(key, expiration, json.dumps(value))

    def delete(self, key: str):
        #Remove a chave do Redis.
        self.client.delete(key)
