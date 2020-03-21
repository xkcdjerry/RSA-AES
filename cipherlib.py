'''
A library to combine RSA and AES to make for faster time.
'''

import aeslib,rsalib

def encode(msg,rsakey):
    key,iv=aeslib.make()
    return rsakey._encrypt(aeslib.pack(key,iv))+aeslib.encrypt(key,iv,msg)
def decode(msg,rsakey):
    head=rsakey._decrypt(msg[:rsalib.OUTCHUNKSIZE])
    key,iv=aeslib.unpack(head)
    return aeslib.decrypt(key,iv,msg[rsalib.OUTCHUNKSIZE:])
