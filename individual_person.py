import json
from typing import Tuple, List, Dict

from abstract_participant import AbstractParticipant
from blockchain import Blockchain
from rsatools import RSATools


class IndividualPerson(AbstractParticipant):
    def __init__(self):
        self.key_wallet = {}

    def __add_key_to_keychain(self, key_name: str, acl_transaction_id: str, private_key: str):
        self.key_wallet.update({key_name: (acl_transaction_id, private_key)})
        # add data to connected device here

    def __add_abstract_transaction_crypted_data(self,
                                                blockchain: Blockchain,
                                                participant_a: AbstractParticipant,
                                                participant_b: AbstractParticipant,
                                                data: str) -> Tuple[str, str]:
        """
        generate RSA keys, crypt the data, add the crypted data to the blochain.
         Returns the private key and the id of the crypted data in the block chain
        :param blockchain:
        :param participant_a:
        :param participant_b:
        :param data:
        :return:  (transaction_id, private_key)
        """
        private_key_for_data, public_key_for_medical_data = RSATools.generate_private_public_key()
        crypted_medical_data = RSATools.crypt_data(data, public_key_for_medical_data)
        medical_data_transaction = blockchain.add_transaction(crypted_medical_data, participant_a, participant_b)
        medical_data_transaction_id = medical_data_transaction.id

        return medical_data_transaction_id, private_key_for_data

    def add_new_acl(self, blockchain: Blockchain, acl_name: str, acl_data : List[Dict]):
        """
        create a new acl entry via acl_data
        :param blockchain: the wordlwide blockchain
        :param acl_name: the name of the acl_name
        :param acl_data: list of {transaction_id : private_key}.
         The private_key decrypt the data in the transaction with the id transaction_id
        :return:
        """
        acl_data_json = json.dumps(acl_data)

        acl_transaction_id, private_key_for_acl = self.__add_abstract_transaction_crypted_data(
            blockchain,
            self,
            self,
            acl_data_json
        )

        self.__add_key_to_keychain(acl_name, acl_transaction_id, private_key_for_acl)

    def add_medical_transaction(self, blockchain: Blockchain, third_party: AbstractParticipant, medical_data: str):
        """

        :param third_party: the doctor/pharmacist/hospital
        :param medical_data: JSON string. The data to store in the blockchain
        :return:
        """

        medical_data_transaction_id, private_key_for_medical_data = \
            self.__add_abstract_transaction_crypted_data(blockchain, self, third_party, medical_data)

        # We straight forward add a element to the keychain to decrypt the data just added to the block chain
        self.add_new_acl(blockchain,
                         f'atomic ACL for {medical_data_transaction_id}',
                         [{medical_data_transaction_id: private_key_for_medical_data}])
