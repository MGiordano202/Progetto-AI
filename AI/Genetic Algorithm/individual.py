import random

class Individual:
    ACTIONS = ['U', 'D', 'L', 'R', 'B'] # Movimento e Bombe

    def __init__(self, sequence):
        self.sequence = sequence


    @classmethod
    def random (cls, seq_length):
        return cls([random.choice(cls.ACTIONS) for _ in range(seq_length)])
