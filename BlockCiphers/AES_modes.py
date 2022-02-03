from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import random

def main(in_file_path):
    with open(in_file_path, mode='rb') as in_file:
        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        cipher = AES.new(key, AES.MODE_ECB)
        out_file = CBC_encrypt(in_file_path, get_blocks(in_fie), cipher, iv)


def get_blocks(bytes):
    pass


def xor_bytes(a, b):
    c = bytearray()
    for (byte_a, byte_b) in (a, b):
        c.append(byte_a ^ byte_b)


def CBC_encrypt(in_file_path, blocks, cipher, iv):
    out_file_path = in_file_path + ".encrypt.txt"
    with open(out_file_path, mode='wb') as out_file:
        for bytes_16 in blocks:
            intermediate = xor_bytes(iv, bytes_16)
            iv = cipher.encrypt(intermediate)
            out_file.write(iv)
    return out_file_path




if __name__ == "__main__":
    main(sys.argv[1])