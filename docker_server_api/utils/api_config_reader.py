""" Configuration reader for the docker compose endpoint """
import os
import json

API_CONFIG_PATH = os.getenv('API_CONFIG_PATH')


class ConfigReader:
    """ Class to handle reading the API config """

    def __init__(self):
        if os.path.isfile(API_CONFIG_PATH) is False:
            raise FileNotFoundError
        self._cfg_path = API_CONFIG_PATH
        cfg = self.__read_config()
        self.compose_file = cfg.get('docker_compose_file_loc')

    def __read_config(self) -> dict:
        """
        Load API config

        :type: None
        :rtype: dict
        :returns: a dict of the JSON config file

        """
        with open(self._cfg_path, 'r', encoding='utf-8') as file:
            return json.load(file)
