import json
from base64 import b64encode, b64decode

class RabbitBody:
    fibo: int
    
    def __init__(self, fibo):
        self.fibo = fibo

    def encode(self):
        dicc = {"fibo": self.fibo}
        return b64encode(json.dumps(dicc).encode())

    @staticmethod
    def decode(encoded):
        dicc = json.loads(b64decode(encoded))
        fibo = dicc["fibo"]
        return RabbitBody(fibo)