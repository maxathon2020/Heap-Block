import os
from typing import Tuple
from Crypto.Cipher import AES

import rsa
from rsa import PrivateKey, PublicKey


class CryptingTools:

    @staticmethod
    def generate_public_private_key() -> Tuple[PublicKey, PrivateKey]:
        return rsa.newkeys(512)

    @staticmethod
    def crypt_data(data: str, public_key: PublicKey) -> dict:
        random_aes_key = os.urandom(16)
        random_aes_iv = os.urandom(16)
        cipher = AES.new(random_aes_key, AES.MODE_EAX, random_aes_iv)

        crypted_data = cipher.encrypt(data.encode('utf8'))
        crypted_aes_key = rsa.encrypt(random_aes_key, public_key)
        crypted_aes_iv = rsa.encrypt(random_aes_iv, public_key)

        return {
            'data': crypted_data,
            'aes_key': crypted_aes_key,
            'aes_iv': crypted_aes_iv,
        }

    @staticmethod
    def uncrypt_data(blockchain_data: dict, private_key: PrivateKey) -> str:
        data_crypted = blockchain_data['data']
        aes_key_crypted = blockchain_data['aes_key']
        aes_iv_crypted = blockchain_data['aes_iv']

        aes_key_uncrypted = rsa.decrypt(aes_key_crypted, private_key)
        aes_iv_uncrypted = rsa.decrypt(aes_iv_crypted, private_key)
        cipher = AES.new(aes_key_uncrypted, AES.MODE_EAX, aes_iv_uncrypted)

        return cipher.decrypt(data_crypted)
