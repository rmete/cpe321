from Crypto.Util.number import getPrime
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Cipher import AES


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

    print(f"Bob's key {alice_key}\nAlice's key {bob_key}\n")
    Alice_msg = "Hi Bob, i'm Alice"
    print(f"Alice: {Alice_msg}")
    Alice_encrypter = AES.new(alice_key, AES.MODE_CBC)
    Alice_sends_to_Bob = Alice_encrypter.encrypt(Alice_msg)

    Bob_encrypter = AES.new(bob_key, AES.MODE_CBC)
    Bob_received_from_Alice = Bob_encrypter.decrypt(Alice_sends_to_Bob)
    print(f"Bob received: {Bob_received_from_Alice}")



if __name__ == "__main__":
    main()
