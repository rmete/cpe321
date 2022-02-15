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
        quotient = old_r // r
        (old_r, r) = (r, old_r - quotient * r)
        (old_s, s) = (s, old_s - quotient * s)
        (old_t, t) = (t, old_t - quotient * t)
    return (old_s, old_t)


def main():
    e = 65537
    p = getPrime(24)
    q = getPrime(16)
    n = p * q
    print(f"n: {n}")
    L = (p - 1)*(q - 1) // GCD(p - 1, q - 1)
    print(f"L: {L}")
    if GCD(e, L ) != 1:
        print("Error: L and e are not coprime")
        quit()

    d = modular_inverse(e, L)[0]
    print(f"d: {d}")

    Bob_says = pad(bytes("Bob", "ascii"), 4).hex()
    print(f"Bobs message as integer {int(Bob_says, 16)}")
    Bob_says_bytes = bytes([int(Bob_says[idx:idx+2], 16) for idx in range(0, len(Bob_says), 2)])
    print(f"Bobs message in bytes: {unpad(Bob_says_bytes, 4).decode('ascii')}")

    Bob_encrypts = pow(int(Bob_says, 16), e, mod=n)
    # print(Bob_encrypts)
    Alice_decrypts = pow(Bob_encrypts, d, mod=n)

    print(f"Alice's decrypted integer: {Alice_decrypts}")
    Alice_decrypts_bytes = Alice_decrypts.to_bytes(4, "big")
    print(f"Alice's decrypted message: {unpad(Alice_decrypts_bytes, 4).decode('ascii')}")



if __name__ == "__main__":
    main()