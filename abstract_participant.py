from rsa import PrivateKey, PublicKey

from cryptingtools import CryptingTools


class AbstractParticipant:
    # should have info to add transaction to the blockchain

    def __init__(self, name: str):
        self.name = name
        self.__public_key, self.__private_key = CryptingTools.generate_public_private_key()

    def _get_private_key(self) -> PrivateKey:
        return self.__private_key

    def get_public_key(self) -> PublicKey:
        return self.__public_key

    def get_name(self) -> str:
        return self.name
