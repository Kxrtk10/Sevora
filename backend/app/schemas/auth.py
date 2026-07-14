from pydantic import BaseModel


class AuthArchitectureResponse(BaseModel):
    status: str
    message: str
