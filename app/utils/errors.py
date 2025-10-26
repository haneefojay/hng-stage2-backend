from fastapi import HTTPException
from typing import Optional, Dict, Any

class APIError(HTTPException):
    def __init__(
        self,
        status_code: int,
        error: str,
        details: Optional[str] = None
    ):
        super().__init__(
            status_code=status_code,
            detail={
                "error": error,
                **({"details": details} if details else {})
            }
        )

class ExternalAPIError(APIError):
    def __init__(self, api_name: str):
        super().__init__(
            status_code=503,
            error="External data source unavailable",
            details=f"Could not fetch data from {api_name}"
        )

class ValidationError(APIError):
    def __init__(self, details: Optional[str] = None):
        super().__init__(
            status_code=400,
            error="Validation failed",
            details=details
        )

class NotFoundError(APIError):
    def __init__(self):
        super().__init__(
            status_code=404,
            error="Country not found"
        )

class InternalServerError(APIError):
    def __init__(self, details: Optional[str] = None):
        super().__init__(
            status_code=500,
            error="Internal server error",
            details=details
        )