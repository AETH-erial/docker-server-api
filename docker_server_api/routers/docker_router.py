import os
import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from docker_server_api.utils.schemas import (ErrorSchema,
                                             Http200Response,
                                             DockerComposeRequest,
                                             GetDockerFiles200,
                                             SetServiceAccountPass)
from docker_server_api.utils.docker_file_handler import DockerFileHandler
from docker_server_api.utils.credential_handler import CypherHandler
from docker_server_api.utils.exceptions import (DirectoryNotFoundError,
                                                BadConfigParameter,
                                                ApiCfgPathNotSet,
                                                ApiCfgFileNotFound,
                                                InvalidComposeRequest,
                                                ApiConfigurationLoadError)

router = APIRouter(
    prefix='/api/v1',
    responses={400: {'model': ErrorSchema}, 401: {'model': ErrorSchema}},
    tags=['example']
)


@router.post('/run-docker-compose',
             responses={200: {'model': Http200Response}},
             description='Endpoint to run a docker-compose.yaml file',
             name='run-docker-compose')
async def run_docker_compose(compose: DockerComposeRequest) -> Http200Response:
    """Run docker-compose on the project associated with parameters in the POST body

    :type compose: DockerComposePost
    :param compose: the docker stack to compose

    :rtype: Http200Response
    :returns: The JSON Data

    :raises HTTPException: If anything goes wrong
    """
    try:
        DockerFileHandler().check_compose_request(compose.stack)

        result = Http200Response(detail='went great')

    except (InvalidComposeRequest, ApiConfigurationLoadError) as error:  # pragma: no cover
        raise HTTPException(status_code=400, detail=f'{error}') from error

    return result


@router.get('/get-all-stacks',
            responses={200: {'model': GetDockerFiles200}},
            description='Endpoint to get the names of all stacks in the stack directory',
            name='get-all-stacks')
def get_all_stacks() -> GetDockerFiles200:
    """
    Return all callable stacks within the appointed docker directory

    :type: None
    :rtype: Http200Response
    :returns: 200 if the directory was found, and a list of stacks to call.
    """
    try:
        stacks = DockerFileHandler().list_stacks()
    except (DirectoryNotFoundError,
            BadConfigParameter,
            ApiCfgPathNotSet,
            ApiCfgFileNotFound) as error:
        raise HTTPException(status_code=400, detail=f'Error loading API config: {error}') from error
    return GetDockerFiles200(stacks=stacks)


@router.post('/assign-service-acc-password',
             responses={200: {'model': Http200Response}},
             description='Endpoint to give the API the encrypted cypher-text of the service account password',
             name='assign_service_account_password')
def assign_service_account_password(payload: SetServiceAccountPass) -> Http200Response:
    """
    Hand the encrypted cyphertext of the service accounts password off to the API

    :type payload: SetServiceAccountPass
    :param payload: the POST body containing the cypher
    :rtype: Http200Response
    :returns: 200 if the cypher text was saved
    :raises HttpException: if there was a problem saving the password

    """
    try:
        CypherHandler().save_cypher(cypher=payload.cypher_text_bytes)
        return Http200Response(detail='Password saved successfully')
    except Exception as err:
        raise HTTPException(status_code=400, detail=f'error: {err}') from err
