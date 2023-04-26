"""
pydantic schemas
"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ErrorSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """Schema for simple Errors"""
    detail: str


class DockerComposePost(BaseModel):  # pylint: disable=too-few-public-methods
    """ Schema for a POST call to run docker compose """
    stack: str


class Http200Response(BaseModel):   # pylint: disable=too-few-public-methods
    """ Response model for 200 response """
    detail: str
