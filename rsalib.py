'''
A wrapper around PyCrypto's RSA feature.
'''

import abc

from Crypto.PublicKey import RSA as rsa
from Crypto.Cipher import PKCS1_OAEP as pkcs

KEYLENTH=2048
OUTCHUNKSIZE=256
INCHUNKSIZE=214

class Key(metaclass=abc.ABCMeta):
    """The base class for RSA keys"""
    
    def __init__(self,key):
        self.key=key
        self.cipher = pkcs.new(key)
    
    def __repr__(self):
        return "<RSA key type '%s'>"%self.__class__.__name__

    def _encrypt(self,b: bytes) -> bytes:
        return self.cipher.encrypt(b)

    
    def _decrypt(self,b: bytes) -> bytes:
        return self.cipher.decrypt(b)
    
    def encrypt(self,b: bytes) -> bytes:
        mem=memoryview(b)
        chunks=[]
        for i in range(0,len(b),INCHUNKSIZE):
            chunks.append(self._encrypt(mem[i:i+INCHUNKSIZE]))
        return b''.join(chunks)
    
    def decrypt(self,b: bytes) -> bytes:
        mem=memoryview(b)
        chunks=[]
        for i in range(0,len(b),OUTCHUNKSIZE):
            chunks.append(self._decrypt(mem[i:i+OUTCHUNKSIZE]))
        return b''.join(chunks)
    
    @abc.abstractmethod
    def dumps(self,private: bool) -> bytes:
        """dump the key into bytes"""
        pass

    def dump(self,private: bool):
        """Dumps the key into the given file"""
        f.write(self.dumps(private))

    @abc.abstractmethod
    def topublic(self):
        """Turn self into a public key"""
        pass

    
    @classmethod
    def gen(cls):
        '''This is very slow,USE SPARCELY!
(keylenth can only be 1024,2048 or 3072)'''
        return PrivateKey(rsa.generate(KEYLENTH))

    @classmethod
    def loads(cls,b:bytes):
        """Loads the RSA key from bytes"""
        key = rsa.importKey(b)
        if key.has_private():
            return PrivateKey(key)
        else:
            return PublicKey(key)

    @classmethod
    def load(cls,f):
        """Loads the RSA key from a file"""
        return cls.loads(f.read())

class PublicKey(Key):
    """A class representing a public key"""

    def dumps(self,private):
        if private:
            raise TypeError("PublicKey cannot be dumped as PrivateKey")
        return self.key.exportKey()
    
    def topublic(self):
        return self
        
class PrivateKey(Key):
    """A class representing a private key"""
    
    def dumps(self,private):
        if not private:
            return self.key.publickey().exportKey()
        else:
            return self.key.exportKey()

    def topublic(self):
        return PublicKey(self.key.publickey())
    
