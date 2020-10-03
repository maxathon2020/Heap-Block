from rsa import PrivateKey, PublicKey

from rsatools import RSATools


class AbstractParticipant:
    # should have info to add transaction to the blockchain

    def __init__(self, name: str):
        self.name = name
        self.public_key, self.private_key = RSATools.generate_public_private_key()

    def __get_private_key(self) -> PrivateKey:
        return self.private_key

    def get_public_key(self) -> PublicKey:
        return self.public_key

    def get_name(self) -> str:
        return self.name
