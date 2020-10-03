import json
from typing import Tuple, List

import more_itertools
from rsa import PrivateKey

from abstract_participant import AbstractParticipant
from blockchain import Blockchain
from cryptingtools import CryptingTools


class IndividualPerson(AbstractParticipant):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keychain = {}
        #  if lost, keychain can be re-generated from the blockchain using self private_key

    def add_key_to_keychain(self, key_name: str, acl_transaction_ids: List[str]):
        assert key_name not in self.keychain.keys(), f'can not add already existing key {key_name}'
        self.keychain.update({key_name: acl_transaction_ids})

    def __add_abstract_transaction_crypted_data(self,
                                                blockchain: Blockchain,
                                                participant_a: AbstractParticipant,
                                                participant_b: AbstractParticipant,
                                                data: str) -> Tuple[str, PrivateKey]:
        """
        generate RSA keys, crypt the data, add the crypted data to the blochain.
         Returns the private key and the id of the crypted data in the block chain
        :param blockchain:
        :param participant_a:
        :param participant_b:
        :param data:
        :return:  (transaction_id, private_key)
        """
        public_key_for_medical_data, private_key_for_data = CryptingTools.generate_public_private_key()
        crypted_medical_data = CryptingTools.crypt_data(data, public_key_for_medical_data)
        medical_data_transaction = blockchain.add_transaction(crypted_medical_data, participant_a, participant_b)
        medical_data_transaction_id = medical_data_transaction.id

        return medical_data_transaction_id, private_key_for_data

    def __add_private_key_to_blockchain(self, blockchain: Blockchain,
                                        medical_data_transaction_id: str,
                                        private_key_for_medical_data: PrivateKey,
                                        third_party=None):
        """
        create a new acl entry via acl_data
        :param blockchain: the wordlwide blockchain
        :param acl_name: the name of the acl_name
        :param acl_data: list of {transaction_id : private_key}.
         The private_key decrypt the data in the transaction with the id transaction_id
        :return:
        """
        third_party = third_party or self
        key_name = f'atomic ACL for {medical_data_transaction_id}'

        acl_data_json = json.dumps({
            'key_name': key_name,
            'private_key': private_key_for_medical_data.save_pkcs1().decode('utf8'),
            'medical_data_transaction_id': medical_data_transaction_id,
        })

        crypted_medical_data = CryptingTools.crypt_data(acl_data_json, self.get_public_key())
        transaction = blockchain.add_transaction(crypted_medical_data, self, third_party)
        transaction_id = transaction.id

        self.add_key_to_keychain(key_name, [transaction_id])
        return transaction_id

    def add_medical_transaction(self, blockchain: Blockchain, third_party: AbstractParticipant, medical_data: str) \
            -> Tuple[str, str]:
        """

        :param blockchain:
        :param third_party: the doctor/pharmacist/hospital
        :param medical_data: JSON string. The data to store in the blockchain
        :return:
        transaction_id for medical_data
        transaction_id for keychain
        """

        medical_data_transaction_id, private_key_for_medical_data = \
            self.__add_abstract_transaction_crypted_data(blockchain, self, third_party, medical_data)

        # We straight forward add a element to the keychain to decrypt the data just added to the block chain
        keychain_transaction_id = self.__add_private_key_to_blockchain(blockchain,
                                                                       medical_data_transaction_id,
                                                                       private_key_for_medical_data,
                                                                       )
        return medical_data_transaction_id, keychain_transaction_id

    def share_medical_data_via_private_keys(self,
                                            blockchain: Blockchain,
                                            key_names: List[str],
                                            third_party_to_share_data_with: AbstractParticipant) \
            -> str:
        # fetch transactions containing the private key we want to shared
        transaction_ids_containing_privates_keys = [self.keychain[a_key_name] for a_key_name in key_names]
        transaction_ids_flattened = more_itertools.flatten(transaction_ids_containing_privates_keys)
        # remove duplicates
        transaction_ids_containing_privates_keys = list(set(transaction_ids_flattened))

        # fetch the private keys we want to shared
        crypted_medical_data_private_keys = blockchain.fetch_transaction_ids(transaction_ids_containing_privates_keys)

        uncrypted_medical_data_private_keys = {
            transaction_id:
                json.loads(
                    CryptingTools.uncrypt_data(
                        crypted_data, self._get_private_key()
                    )
                )
            for transaction_id, crypted_data in crypted_medical_data_private_keys.items()
        }

        data_to_share_uncrypted = json.dumps(uncrypted_medical_data_private_keys)
        data_to_share_crypted = CryptingTools.crypt_data(data_to_share_uncrypted,
                                                         third_party_to_share_data_with.get_public_key())
        created_transaction = blockchain.add_transaction(data_to_share_crypted, self, third_party_to_share_data_with)
        return created_transaction.id
