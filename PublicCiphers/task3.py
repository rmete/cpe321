from Crypto.Util.number import getPrime
from Crypto.Util.number import GCD
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES


def modular_inverse(a, b):
    (old_r, r) = (a, b)
    (old_s, s) = (1, 0)
    (old_t, t) = (0, 1)
    while r != 0:
        quotient = old_r / r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t)
    return (old_s, old_t)


def main():
    e = 65537
    p = getPrime(16)
    q = getPrime(16)
    n = p * q
    L = (p - 1)*(q - 1) // GCD(p - 1, q - 1)
    if L % e == 0:
        print("Error: L and e are not coprime")
        quit()

    d = modular_inverse(e, L)[0]

    Bob_says = pad(bytes("Bob", "ascii"), 4).hex()
    print(Bob_says)
    print(unpad(bytes([int(Bob_says, 16)]), 4).decode("ascii"))


    Bob_encrypts = pow(int(Bob_says, 16), e, mod=n)
    # print(Bob_encrypts)
    Alice_decrypts = pow(Bob_encrypts, d, mod=n)
    print(Alice_decrypts)
    print(bytes([Alice_decrypts]).decode("ascii"))






if __name__ == "__main__":
    main()