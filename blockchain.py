from typing import Union, List

from abstract_participant import AbstractParticipant
from transaction import Transaction

import hashlib
import json
from time import time


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.pending_transactions = []

        self.new_block(previous_hash="Initial block : blockchain begins here",
                       proof=100)

        # Create a new block listing key/value pairs of block information in a JSON object.
        # Reset the list of pending transactions & append the newest block to the chain.

    def __str__(self) -> str:
        return json.dumps({
            'chain': [{
                'index': chain_element['index'],
                'content': [a_transaction.to_dict() for a_transaction in chain_element['transactions']]
            } for chain_element in self.chain]
        })

    def new_block(self, proof, previous_hash=None):
        try:
            new_hash = self.hash(self.chain[-1]['transactions'][0].data)
        except:
            new_hash = None
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.pending_transactions,
            'proof': proof,
            'previous_hash': previous_hash or new_hash,
        }
        self.pending_transactions = []
        self.chain.append(block)

        return block

    # Search the blockchain for the most recent block.

    @property
    def last_block(self):
        return self.chain[-1]

    # Add a transaction with relevant info to the 'blockpool' - list of pending tx's.
    def add_transaction(self, data, participant_a: AbstractParticipant,
                        participant_b: AbstractParticipant) -> Transaction:
        transaction = Transaction(data, participant_a, participant_b)
        self.pending_transactions.append(transaction)
        return transaction

    def fetch_transaction_ids(self, transaction_ids: List[str]) -> dict:
        """

        :param transaction_ids:
        :return: {transacton_id: content}
        """
        found_transactions= {}
        for block in self.chain:
            for a_transaction in block['transactions']:
                if a_transaction.id in transaction_ids:
                    found_transactions.update({a_transaction.id: a_transaction.data})

        return found_transactions

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()

        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()

        return hex_hash
