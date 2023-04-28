""" Handler for docker directory related tasks """
import os
import subprocess
from docker_server_api.utils.api_config_reader import ConfigReader
from docker_server_api.utils.exceptions import (DirectoryNotFoundError,
                                                BadConfigParameter,
                                                ApiCfgPathNotSet,
                                                ApiCfgFileNotFound,
                                                ApiConfigurationLoadError,
                                                InvalidComposeRequest)


class DockerFileHandler:
    """ File handler for docker related tasks """
    def __init__(self) -> None:
        """
        Init for the DockerFileHandler class

        :type: None
        :rtype: None

        """
        try:
            self._cfg = ConfigReader()
        except (DirectoryNotFoundError,
                BadConfigParameter,
                ApiCfgPathNotSet,
                ApiCfgFileNotFound) as error:
            raise ApiConfigurationLoadError(f'error loading the API config: {type(error).__name__}') from error

    def list_stacks(self) -> list:
        """
        List all stacks from the appointed docker control directory

        :type: None
        :rtype: list
        :returns: a list of the stacks to run

        """
        docker_files = self._cfg.compose_files
        return os.listdir(docker_files)

    def check_compose_request(self, req: str) -> bool:
        """
        Evaluate a docker compose request

        :type req: str
        :param req: the stack to compare the request against
        :rtype: bool
        :returns: True if the request checks out
        :raises TypeError: if req isn't a str
        :raises InvalidComposeRequest: if the requested stack doesn't exist

        """
        if not isinstance(req, str):
            raise TypeError(f'req should have been a str but got a: {type(req).__name__}')
        stacks = self.list_stacks()
        if req not in stacks:
            raise InvalidComposeRequest(f'stack: {req} not in {stacks}. Check stacks at: {self._cfg.compose_files}')
        return True

    def run_docker_compose(self, req: str) -> int:
        """
        Run a docker compose file

        :type req: str
        :param req: the docker stack to spin up
        :rtype: int
        :returns: 0 if the request was ok, anything else is a failed request

        """
        command = f'cd {self._cfg.compose_files}/{req} && docker compose up'
        subprocess.run(command, shell=True)
        return 0
