from hashlib import blake2b
from typing import Optional
from os import urandom
import base64


class Hash:
    '''
    A class to hash data using the Blake2b algorithm
    '''

    def __init__(self):
        pass

    def hash(self, data: bytes = urandom(8), digest_size: Optional[int] = None) -> str:
        """ 
        We use blake2b bcs i like William Blake (https://en.wikipedia.org/wiki/William_Blake)
        """        
        return blake2b(data=data, digest_size=digest_size or 16).hexdigest()

    def base64(self, data: bytes = urandom(8)) -> str:
        """ 
        We use base64 bcs i like base64 (for CF clearance)
        """
        return base64.b64encode(data).decode()

