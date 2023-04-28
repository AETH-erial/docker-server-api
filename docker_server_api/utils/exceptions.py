""" Custom exception types """


class DirectoryNotFoundError(Exception):
    """ Exception type for a nonexistent directory """
    pass


class BadConfigParameter(Exception):
    """ Exception type for a bad configuration parameter """
    pass


class ApiCfgPathNotSet(Exception):
    """ Exception type in the event that the API_CONFIG_PATH env var isnt set """
    pass


class ApiCfgFileNotFound(Exception):
    """ Exception type for a nonexistent API config file """
    pass


class ApiConfigurationLoadError(Exception):
    """ Coverall exception type to raise in the event of a config loading error """
    pass


class InvalidComposeRequest(Exception):
    """ Exception type for an invalid docker-compose request """
    pass


class CypherNotSet(Exception):
    """ Exception type for an unset cypher """
    pass

