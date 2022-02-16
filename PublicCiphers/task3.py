from Cryptodome.Util.number import GCD
from Cryptodome.Util.number import getPrime
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import AES


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

    Mallory_key = pad(bytes("Mal", "ascii"), 4).hex()
    print(f"if Mallory subsitutes her own key '{Mallory_key}' which is: {int(Mallory_key, 16)} for Bob's message")
    Mallory_encrypts = pow(int(Mallory_key, 16), e, mod=n)
    Alice_decrypts = pow(Mallory_encrypts, d, mod=n)
    Alice_decrypts_bytes = Alice_decrypts.to_bytes(4, "big")
    print(f"Allice receives {Alice_decrypts} and will decrypt the intercepted message to {unpad(Alice_decrypts_bytes, 4).decode('ascii')}")
    print("Alice is now using Mallory's key")



if __name__ == "__main__":
    main()


def main1():
    e = 65537       # Alice sends e
    p = getPrime(24)
    q = getPrime(16)
    n = p * q       # Alice sends n

    # Bob computes s, select s to be n -1 
    bob_s = n -1

    # Bob computes c using defined s from above and sends it back to Alice
    c = (bob_s ** e) % n

    # # Create a key for Bob using selected s value
    # bob_hasher = SHA256.new(data = str(bob_s).encode())
    # bob_key = bob_hasher.digest()[:16]

    # Mallory modifies c 
    # By setting c to 1, Mallory knows that Alice's key will also have to be 1
    # Note: Mallory also knows the value of n and e
    Mallory_c = 1

    # Alice computes s using the modified c from Mallory
    # Because c is now 1, Mallory knows that s will compute to be 1
    L = (p - 1)*(q - 1) // GCD(p - 1, q - 1)
    d = modular_inverse(e, L)[0]
    s = (Mallory_c ** d) % n 

    # Alice creates an encriptor
    alice_hasher = SHA256.new()
    alice_hasher.update(bytes(s))
    alice_key = alice_hasher.digest()[:16]
    alice_iv = alice_hasher.digest()[16:32]
    alice_encrypter = AES.new(alice_key, AES.MODE_CBC, alice_iv)

    # Alice sends encripted message c
    alice_msg = pad(bytes("Hi Bob!", "ascii"), 16)
    c0 = alice_encrypter.encrypt(alice_msg)

    # Mallory swooping in again, knowing that s will be 1
    # Because of this info, mallory can create their own key and encryption
    # Mallory can now decrpyt messages as well as send them 
    mallory_hasher = SHA256.new()
    mallory_hasher.update(bytes(1))
    mallory_key = mallory_hasher.digest()[:16]
    mallory_iv = mallory_hasher.digest()[16:32]
    mallory_encrypter = AES.new(mallory_key, AES.MODE_CBC, mallory_iv)
    intercepted_msg = unpad(mallory_encrypter.decrypt(c0), 16).decode()
    print(f"Mallory intercepted the message {intercepted_msg}")



if __name__ == "__main__":
    main1()