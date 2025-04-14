from typing import Optional, List

from fastapi.responses import JSONResponse


class ErrorResponse(JSONResponse):
    message: str
    code: int
    errors: Optional[List[str]] = None
