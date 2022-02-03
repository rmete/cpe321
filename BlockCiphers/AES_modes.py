from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import random

def main(in_file_path):
    with open(in_file_path, mode='rb') as in_file:
        file_bytes = in_file.read()
        blocks = get_blocks(file_bytes)
        print(blocks)
        # key = get_random_bytes(16)
        # iv = get_random_bytes(16)
        # cipher = AES.new(key, AES.MODE_ECB)
        # out_file = CBC_encrypt(in_file_path, get_blocks(in_file), cipher, iv)


def pkcs7_pad(to_pad, m):
    if len(to_pad) % m != 0:
        pad_with = (m * (len(to_pad) // m + 1)) - len(to_pad)
        to_pad = to_pad + bytes([pad_with] * pad_with)
    return to_pad

def get_blocks(file_as_bytes):
    file_as_bytes = pkcs7_pad(file_as_bytes, 16)
    blocks = [bytes(file_as_bytes[x - 16: x]) for x in range(16, len(file_as_bytes) + 1, 16)]
    return blocks


def xor_bytes(a, b):
    c = bytearray()
    for (byte_a, byte_b) in (a, b):
        c.append(byte_a ^ byte_b)
    return c


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