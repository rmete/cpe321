from Cryptodome.Util.number import getPrime
from Cryptodome.Util.Padding import pad, unpad
from Cryptodome.Random import get_random_bytes
from Cryptodome.Hash import SHA256
from Cryptodome.Cipher import AES



def main():
    p = 37
    g = 5

    Alice_prime = getPrime(16)
    Bob_prime = getPrime(16)
    print(f"Alice's prime: {Alice_prime}")
    print(f"Bob's prime: {Bob_prime}")

    Alice_public = pow(g, Alice_prime) % p
    Bob_public = pow(g, Bob_prime) % p

    Alice_shared_secret = bytes(pow(Bob_public, Alice_prime) % p)
    Bob_shared_secret = bytes(pow(Alice_public, Bob_prime) % p)

    Alice_hasher = SHA256.new()
    Alice_hasher.update(Alice_shared_secret)
    alice_key = Alice_hasher.digest()

    Bob_hasher = SHA256.new()
    Bob_hasher.update(Bob_shared_secret)
    bob_key = Bob_hasher.digest()

    iv = get_random_bytes(16)

    print(f"Bob's key {alice_key}\nAlice's key {bob_key}\n")
    Alice_msg = pad(bytes("Hi Bob, i'm Alice", "ascii"), 16)
    print(f"Alice: {unpad(Alice_msg, 16)}")
    Alice_encrypter = AES.new(alice_key, AES.MODE_CBC, iv=iv)
    Alice_sends_to_Bob = Alice_encrypter.encrypt(Alice_msg)

    Bob_encrypter = AES.new(bob_key, AES.MODE_CBC, iv=iv)
    Bob_received_from_Alice = Bob_encrypter.decrypt(Alice_sends_to_Bob)
    print(f"Bob received: {unpad(Bob_received_from_Alice, 16)}")



if __name__ == "__main__":
    main()
