from datetime import datetime
import hashlib


class Transaction:
    def __init__(self, data, participant_a, participant_b):
        self.id = self.compute_hash_time()
        self.data = data
        self.participant_a = participant_a
        self.participant_b = participant_b

    def compute_hash_time(self):
        timestamp_now = str(datetime.now()).encode()
        return hashlib.md5(timestamp_now).hexdigest()
