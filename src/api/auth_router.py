"""Endpoints de Autenticación."""
from fastapi import APIRouter, HTTPException, Depends
from src.schemas.dto import UserSignup, UserLogin, UserRead, AuthToken
from src.repositories.user_repository import UserRepository
from src.services.auth_service import AuthService
from src.db import get_connection, return_connection
from src.utils.dependencies import get_current_user

router = APIRouter(prefix="/auth", tags=["auth"])

user_repo = UserRepository()
auth_service = AuthService(user_repo)


@router.post("/signup", response_model=UserRead)
async def signup(user: UserSignup):
    conn = get_connection()
    try:
        result = await auth_service.signup(conn, user.email, user.password)
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        return result
    finally:
        return_connection(conn)


@router.post("/login", response_model=AuthToken)
async def login(user: UserLogin):
    conn = get_connection()
    try:
        result = await auth_service.login(conn, user.email, user.password)
        if "error" in result:
            raise HTTPException(status_code=401, detail=result["error"])
        return {"access_token": result["token"], "token_type": "bearer"}
    finally:
        return_connection(conn)


@router.get("/me", response_model=UserRead)
async def get_profile(current_user: dict = Depends(get_current_user)):
    """Obtener perfil del usuario autenticado."""
    return {"id": int(current_user["sub"]), "email": current_user["email"]}
