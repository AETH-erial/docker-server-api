import subprocess
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel  # pylint: disable=no-name-in-module
from docker_server_api.utils.schemas import ErrorSchema, Http200Response, DockerComposePost
from docker_server_api.utils.api_config_reader import ConfigReader


router = APIRouter(
    prefix='/api/v1',
    responses={400: {'model': ErrorSchema}, 401: {'model': ErrorSchema}},
    tags=['example']
)


@router.post('/run-docker-compose',
             responses={200: {'model': Http200Response}},
             description='This is an example',
             name='Example endpoint')
async def run_docker_compose(compose: DockerComposePost) -> Http200Response:
    """Run docker-compose on the project associated with parameters in the POST body

    :type compose: DockerComposePost
    :param compose: the docker stack to compose

    :rtype: Http200Response
    :returns: The JSON Data

    :raises HTTPException: If anything goes wrong
    """
    try:
        cfg = ConfigReader()
        process = subprocess.Popen([''])

        result = Http200Response(detail='went great')

    except Exception as error:  # pragma: no cover
        raise HTTPException(status_code=400, detail=f'{error}') from error

    return result
