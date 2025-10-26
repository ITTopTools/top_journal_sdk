import httpx

from starlette.exceptions import HTTPException

from .data import config

class authManager:
    def __init__(self):
        pass

    
    async def get_csrf_token(self):
        async with httpx.AsyncClient(
            base_url=config.BASE_API_URL, timeout=5) as _client:
            
            headers = {
                        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:142.0) Gecko/20100101 Firefox/142.0",
                        "Accept": "application/json, text/plain, */*",
                        "Content-Type": "application/json",
                        "Referer": "https://journal.top-academy.ru/",  
                        "Origin": "https://journal.top-academy.ru",
                    }
            
            request = await _client.get(config.AUTH_URL, headers=headers)
                
            jwt_token = request.cookies.get("_csrf")
            
            if jwt_token: # TODO - Validation
                return jwt_token
            
            raise HTTPException(403, "Invalid jwt token!")
