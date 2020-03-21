import os

from Crypto.Cipher import AES as aes
from Crypto.Util import Padding as pad

BLOCKSIZE=aes.block_size
KEYSIZE=32
IVSIZE =16
HEADSIZE=KEYSIZE+IVSIZE

def encrypt(key,iv,msg):
    cipher=aes.new(key,aes.MODE_CBC,iv)
    return cipher.encrypt(pad.pad(msg,BLOCKSIZE))

def decrypt(key,iv,msg):
    cipher=aes.new(key,aes.MODE_CBC,iv)
    return pad.unpad(cipher.decrypt(msg),BLOCKSIZE)


def make():
    # key,iv
    return os.urandom(KEYSIZE),os.urandom(IVSIZE)
def unpack(b):
    if len(b)!=HEADSIZE:
        raise ValueError("Lenth of b must be %d"%HEADSIZE)
    return b[:KEYSIZE],b[-IVSIZE:]
def pack(key,iv):
    return key+iv
