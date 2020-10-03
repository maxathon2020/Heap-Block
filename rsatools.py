from typing import Tuple

import rsa
from rsa import PrivateKey, PublicKey


class RSATools:

    @staticmethod
    def generate_public_private_key() -> Tuple[PublicKey, PrivateKey]:
        return rsa.newkeys(512)

    @staticmethod
    def crypt_data(data: str, public_key: PublicKey) -> bytes:
        return rsa.encrypt(data.encode('utf8'), public_key)

    @staticmethod
    def uncrypt_data(crypted_data: bytes, private_key: PrivateKey) -> str:
        return rsa.decrypt(crypted_data, private_key).decode('utf8')
