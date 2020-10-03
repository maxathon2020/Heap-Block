import json
from typing import Tuple, List

from rsa import PrivateKey

from abstract_participant import AbstractParticipant
from blockchain import Blockchain
from rsatools import RSATools
from transaction import Transaction


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
        public_key_for_medical_data, private_key_for_data = RSATools.generate_public_private_key()
        crypted_medical_data = RSATools.crypt_data(data, public_key_for_medical_data)
        medical_data_transaction = blockchain.add_transaction(crypted_medical_data, participant_a, participant_b)
        medical_data_transaction_id = medical_data_transaction.id

        return medical_data_transaction_id, private_key_for_data

    def __add_private_key_to_blockchain(self, blockchain: Blockchain,
                                        medical_data_transaction_id: str,
                                        private_key_for_medical_data: PrivateKey):
        """
        create a new acl entry via acl_data
        :param blockchain: the wordlwide blockchain
        :param acl_name: the name of the acl_name
        :param acl_data: list of {transaction_id : private_key}.
         The private_key decrypt the data in the transaction with the id transaction_id
        :return:
        """
        key_name = f'atomic ACL for {medical_data_transaction_id}'

        acl_data_json = json.dumps({
            'key_name': key_name,
            'private_key': private_key_for_medical_data,
            'medical_data_transaction_id': medical_data_transaction_id,
        })

        transaction_id, private_key_for_acl = self.__add_abstract_transaction_crypted_data(
            blockchain,
            self,
            self,
            acl_data_json
        )

        self.add_key_to_keychain(key_name, [transaction_id])

    def add_medical_transaction(self, blockchain: Blockchain, third_party: AbstractParticipant, medical_data: str):
        """

        :param blockchain:
        :param third_party: the doctor/pharmacist/hospital
        :param medical_data: JSON string. The data to store in the blockchain
        :return:
        """

        medical_data_transaction_id, private_key_for_medical_data = \
            self.__add_abstract_transaction_crypted_data(blockchain, self, third_party, medical_data)

        # We straight forward add a element to the keychain to decrypt the data just added to the block chain
        self.__add_private_key_to_blockchain(blockchain, medical_data_transaction_id, private_key_for_medical_data)

    def share_medical_data_via_private_keys(self,
                                            blockchain: Blockchain,
                                            key_names: List[str],
                                            third_party_to_share_data_with: AbstractParticipant) \
            -> Transaction:
        # fetch transactions containing the private key we want to shared
        transaction_ids_containing_privates_keys = [self.keychain[a_key_name] for a_key_name in key_names]
        # remove duplicates
        transaction_ids_containing_privates_keys = list(set(transaction_ids_containing_privates_keys))

        # fetch the private keys we want to shared
        crypted_medical_data_private_keys = blockchain.fetch_transaction_ids(transaction_ids_containing_privates_keys)

        uncrypted_medical_data_private_keys = {
            crypted_data['medical_data_transaction_id']:
                RSATools.uncrypt_data(
                    crypted_data['private_key'], self.__get_private_key()
                )
            for (transaction_id, crypted_data) in crypted_medical_data_private_keys.items()
        }

        data_to_share_uncrypted = json.dumps(uncrypted_medical_data_private_keys)
        data_to_share_crypted = RSATools.crypt_data(data_to_share_uncrypted,
                                                    third_party_to_share_data_with.get_public_key())
        return blockchain.add_transaction(data_to_share_crypted, self, third_party_to_share_data_with)
