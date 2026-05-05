"""Servicio de Autenticación."""
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta
from src.services.base_service import BaseService
from src.utils.jwt import create_access_token, decode_access_token


class AuthService(BaseService):
    """Servicio de autenticación con hash de passwords."""

    def __init__(self, user_repository):
        super().__init__(user_repository)

    @staticmethod
    def hash_password(password: str) -> str:
        """Hash de contraseña con salt."""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
        return f"{salt}${pwd_hash.hex()}"

    @staticmethod
    def verify_password(password: str, password_hash: str) -> bool:
        """Verificar contraseña."""
        try:
            salt, pwd_hash = password_hash.split("$")
            computed = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100000)
            return hmac.compare_digest(computed.hex(), pwd_hash)
        except (ValueError, AttributeError):
            return False

    async def signup(self, conn, email: str, password: str) -> dict:
        """Registrar usuario."""
        existing = await self.repo.get_by_email(conn, email)
        if existing:
            return {"error": "Email already registered"}
        
        pwd_hash = self.hash_password(password)
        return await self.repo.create(conn, {"email": email, "password_hash": pwd_hash})

    async def login(self, conn, email: str, password: str) -> dict:
        """Autenticar usuario."""
        user = await self.repo.get_by_email(conn, email)
        if not user or not self.verify_password(password, user["password_hash"]):
            return {"error": "Invalid credentials"}
        
        token = create_access_token({"sub": str(user["id"]), "email": user["email"]})
        return {"id": user["id"], "email": user["email"], "token": token}
