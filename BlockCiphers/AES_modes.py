from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
import sys
import random

def main(in_file_path):
    with open(in_file_path, mode='rb') as in_file:
        file_bytes = in_file.read()
        blocks = get_blocks(file_bytes)
        # print(blocks)


        key = get_random_bytes(16)
        iv = get_random_bytes(16)
        # According to docs we have to create new cipher object for each encryption/decryption

        out_bytes = CBC_encrypt(blocks, iv)
        print(CBC_decrypt(out_bytes, iv))


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
    for idx in range(16):
        c.append(a[idx] ^ b[idx])
    return c


def CBC_encrypt(blocks, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = bytearray()
    for bytes_16 in blocks:
        intermediate = xor_bytes(iv, bytes_16)
        iv = cipher.encrypt(intermediate)
        encrypted.push(iv)
    return encrypted


def CBC_decrypt(blocks, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = bytearray()
    for bytes_16 in blocks:
        intermediate = cipher.decrypt(bytes_16)
        decrypted.push(xor_bytes(iv, intermediate))
        iv = bytes_16
    return decrypted



if __name__ == "__main__":
    main(sys.argv[1])