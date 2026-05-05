"""Dependencias de FastAPI."""
from fastapi import HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from src.utils.jwt import decode_access_token

security = HTTPBearer()


async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)) -> dict:
    """Validar JWT y retornar usuario actual."""
    token = credentials.credentials
    payload = decode_access_token(token)
    
    if "error" in payload:
        raise HTTPException(status_code=401, detail=payload["error"])
    
    return payload
