from datetime import datetime
import hashlib

from abstract_participant import AbstractParticipant


class Transaction:
    def __init__(self, data, participant_a: AbstractParticipant, participant_b: AbstractParticipant):
        self.id = self.compute_hash_time()
        self.data = data
        self.participant_a = participant_a
        self.participant_b = participant_b

    def compute_hash_time(self):
        timestamp_now = str(datetime.now()).encode()
        return hashlib.md5(timestamp_now).hexdigest()

    def to_dict(self) -> dict:
        return {
            'id': self.id,
            'data': str(self.data),
            'participant_a': self.participant_a.get_name(),
            'participant_b': self.participant_b.get_name(),
        }
