"""
pydantic schemas
"""
from pydantic import BaseModel  # pylint: disable=no-name-in-module


class ErrorSchema(BaseModel):  # pylint: disable=too-few-public-methods
    """Schema for simple Errors"""
    detail: str


class DockerComposeRequest(BaseModel):  # pylint: disable=too-few-public-methods
    """ Schema for a POST call to run docker compose """
    stack: str
    key: bytes


class Http200Response(BaseModel):   # pylint: disable=too-few-public-methods
    """ Response model for 200 response """
    detail: str


class GetDockerFiles200(BaseModel):
    """ Response model for a call to retrieve all docker stacks """
    stacks: list[str]


class SetServiceAccountPass(BaseModel):
    """ Model for giving the API the encrypted cypher text of the service accounts password """
    cypher_text_bytes: bytes
