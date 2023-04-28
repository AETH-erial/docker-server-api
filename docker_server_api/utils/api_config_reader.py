""" Configuration reader for the docker compose endpoint """
import os
import json
from docker_server_api.utils.exceptions import (DirectoryNotFoundError,
                                                BadConfigParameter,
                                                ApiCfgPathNotSet,
                                                ApiCfgFileNotFound)
from docker_server_api.utils.enums import ApiConfigFields
from const import API_CONFIG_PATH


class ConfigReader:
    """ Class to handle reading the API config """

    def __init__(self):
        if API_CONFIG_PATH is None:
            raise ApiCfgPathNotSet(f'env variable: API_CONFIG_PATH is not set')
        if os.path.isfile(API_CONFIG_PATH) is False:
            raise ApiCfgFileNotFound(f'filepath: {API_CONFIG_PATH} doesnt resolve on the host.')
        self._cfg_path = API_CONFIG_PATH
        cfg = self.__read_config()
        if self.__validate_conf_fields(cfg) is True:
            self.compose_files = cfg.get('docker_compose_fp')
            self.__assert_docker_dir_exists()

    def __read_config(self) -> dict:
        """
        Load API config

        :type: None
        :rtype: dict
        :returns: a dict of the JSON config file

        """
        with open(self._cfg_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    @staticmethod
    def __validate_conf_fields(cfg: dict) -> bool:
        """
        Validated the fieldnames in the api config file

        :type cfg: dict
        :param cfg: the dictionary representation of the configuration
        :rtype: bool
        :returns: True if the config is OK

        """
        if not isinstance(cfg, dict):
            raise TypeError(f'cfg should have been a dict but got a: {type(cfg).__name__}')
        for key in cfg.keys():
            try:
                ApiConfigFields(key)
            except ValueError as err:
                raise BadConfigParameter(f'config parameter: {key} not a valid value. See: {ApiConfigFields}') from err
        return True

    def __assert_docker_dir_exists(self) -> bool:
        """
        Assert that the directory with your docker files is accessible/real

        :type: None
        :rtype: bool
        :returns: True if the directory exists
        :raises DirectoryNotFoundError: if the directory doesn't exist

        """
        if os.path.isdir(self.compose_files) is False:
            raise DirectoryNotFoundError(f'directory: {self.compose_files} does not resolve on the hosts filesystem')
        return True
