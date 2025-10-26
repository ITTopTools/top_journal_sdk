import httpx
from .auth import authManager

class client:
    def __init__(self, client: httpx.AsyncClient):
        self.client: httpx.AsyncClient = client
        self.auth: object = authManager()

    def schedule(token: str, date: str):
        pass
    
    def homework(token: str, date: str):
        pass

    def close(self):
        if client:
            self.client.aclose()
            return
        
