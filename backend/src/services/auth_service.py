from typing import Optional
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from ..config.settings import settings
from ..auth.jwt_handler import verify_token, TokenData


class AuthService:
    """
    Service class for handling authentication operations.
    """

    def __init__(self):
        self.secret_key = settings.jwt_secret
        self.algorithm = "HS256"

    def verify_token(self, token: str) -> Optional[TokenData]:
        """
        Verify a JWT token and return the decoded data.
        """
        return verify_token(token)

    def decode_user_id_from_token(self, token: str) -> Optional[str]:
        """
        Extract and return the user_id from a JWT token.
        """
        token_data = self.verify_token(token)
        if token_data:
            return token_data.user_id
        return None


# Initialize auth service instance
auth_service = AuthService()


def get_current_user_from_token(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())) -> str:
    """
    Dependency to extract user_id from JWT token in Authorization header.
    """
    token = credentials.credentials
    user_id = auth_service.decode_user_id_from_token(token)

    if user_id is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user_id