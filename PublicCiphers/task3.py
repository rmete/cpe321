from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


def main():
    e = 65537
    p = getPrime(24)
    q = getPrime(16)
    n = p * q




if __name__ == "__main__":
    main()