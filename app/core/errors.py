from email import message
from enum import Enum
from typing import Optional, Dict, Any
from fastapi import HTTPException, status

class ErrorCode(str, Enum):
    """Standerized error codes"""
    # Authentication
    INVALID_CREDENTIALS = "INVALID_CREDENTIALS"
    TOKEN_EXPIRED = "TOKEN_EXPIRED"
    UNAUTHORIZED = "UNAUTHORIZED"
    ACCOUNT_LOCKED = "ACCOUNT_LOCKED"
    
    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_EMAIL = "INVALID_EMAIL"
    INVALID_PHONE = "INVALID_PHONE"
    
    # Resources
    USER_NOT_FOUND = "USER_NOT_FOUND"
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    ALREADY_EXISTS = "ALREADY_EXISTS"
    EMAIL_ALREADY_EXISTS = "EMAIL_ALREADY_EXISTS"
    
    # Server
    INTERNAL_ERROR = "INTERNAL_ERROR"
    DATABASE_ERROR = "DATABASE_ERROR"


class AppException(HTTPException):
    """Personnalized exception with error code"""
    
    def __init__(
        self,
        error_code: ErrorCode,
        status_code: int = status.HTTP_400_BAD_REQUEST,
        params: Optional[Dict[str, Any]] = None
    ):
        detail = {
            "error_code": error_code.value,
            "params": params or {}
        }
        super().__init__(status_code=status_code, detail=detail)

# Specific exceptions
class UnauthorizedError(AppException):
    def __init__(self, message: str = "Authentification requise"):
        super().__init__(
            error_code=ErrorCode.UNAUTHORIZED,
            status_code=status.HTTP_401_UNAUTHORIZED,
            params={"message": message}
        )

class ForbiddenError(AppException):
    def __init__(self, resource: str = "resource", message: str = "Accès non autorisé"):
        super().__init__(
            error_code=ErrorCode.FORBIDDEN,
            status_code=status.HTTP_403_FORBIDDEN,
            params={
                "resource": resource,
                "message": message
            }
        )

class AccountLockedError(AppException):
    def __init__(self):
        super().__init__(
            error_code=ErrorCode.ACCOUNT_LOCKED,
            status_code=status.HTTP_423_LOCKED,
            params={}
        )

class EmailAlreadyExistsError(AppException):
    def __init__(self, email: str):
        super().__init__(
            error_code=ErrorCode.EMAIL_ALREADY_EXISTS,
            status_code=status.HTTP_409_CONFLICT,
            params={
                "email": email,
                "message": "Cet email est déjà utilisé"
            }
        )

class UserNotFoundError(AppException):
    def __init__(self, user_id: int):
        super().__init__(
            error_code=ErrorCode.USER_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            params={
                "user_id": user_id,
                "message": "Utilisateur inconnu"
            }
        )

class ResourceNotFoundError(AppException):
    def __init__(self, message: str = "Ressource inconnue"):
        super().__init__(
            error_code=ErrorCode.RESOURCE_NOT_FOUND,
            status_code=status.HTTP_404_NOT_FOUND,
            params={
                "message": message
            }
        )

class AlreadyExistsError(AppException):
    def __init__(self, message: str = "Cette ressource existe déjà"):
        super().__init__(
            error_code = ErrorCode.ALREADY_EXISTS,
            status_code = status.HTTP_409_CONFLICT,
            params = {
                "message": message
            }
        )