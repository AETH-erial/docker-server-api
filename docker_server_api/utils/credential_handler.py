""" Class to handle credential reading and writing """
import os
import cryptography
from cryptography.fernet import Fernet
from const import CRED_CYPHER_LOC
from docker_server_api.utils.exceptions import CypherNotSet


class CypherHandler:
    """ Class to handle decryption related tasks """
    def __init__(self, key: bytes) -> None:
        """
        Init for DecryptionHandler class

        :type key: bytes
        :param key: the bytes representation of the key to decrypt a cypher with
        :rtype: None
        :raises TypeError: if key isn't a bytes object
        """
        self._key = Fernet(bytes)
        self._cypher_text = CRED_CYPHER_LOC

    def read_pass(self) -> str:
        """
        Read and decrypt the cyphered credential

        :type: None
        :rtype: str
        :returns: the string of the decrypted password
        :raises CypherNotSet: if the cypher.pass file is empty

        """
        with open(f'{self._cypher_text}', 'rb') as file:
            data = file.read()
        return self._key.decrypt(data)

    def save_cypher(self, cypher: bytes) -> int:
        """
        save a cypher to the API's cypher storage location

        :type cypher: bytes
        :param cypher: the encrypted byte string to be saved
        :rtype: int
        :returns: 0 if the file was saved successfully
        :raises TypeError: if cypher isnt a bytes
        :raises PermissionsError: if the file couldnt be written to

        """
        if not isinstance(cypher, bytes):
            raise TypeError(f'cypher should have been bytes but got a: {type(cypher).__name__}')
        with open(f'{self._cypher_text}', 'wb') as file:
            file.write(cypher)
