from typing import Tuple


class RSATools:

    @staticmethod
    def generate_private_public_key() -> Tuple[str, str]:
        # rsa magic to generate private_key, publicc_key
        return (1, 2)

    @staticmethod
    def crypt_data(public_key: str, data: str) -> str:
        # RSA magic here
        return data
