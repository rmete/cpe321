from Crypto.Util.number import getPrime
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
from Crypto.Hash import SHA256
from Crypto.Cipher import AES
from Crypto.Cipher import AES

# Part 1
def main_1():
    p = 37
    g = 5

    # Get prime for Alice and Bob
    Alice_prime = getPrime(16)
    Bob_prime = getPrime(16)
    print(f"Alice's prime: {Alice_prime}")
    print(f"Bob's prime: {Bob_prime}")

    Alice_public = pow(g, Alice_prime) % p
    Bob_public = pow(g, Bob_prime) % p

    # Mallory's modifications
    Alice_public = p
    Bob_public = p

    # Because Mallory changed public to 'p', it will always mod to 0 no matter the prime
    Alice_shared_secret = bytes(pow(Bob_public, Alice_prime) % p)
    Bob_shared_secret = bytes(pow(Alice_public, Bob_prime) % p)

    # Mallory can now be sneaky
    Mallory_stolen_secret = bytes(0)
    Mallory_hasher = SHA256.new()
    Mallory_hasher.update(Mallory_stolen_secret)
    mallory_key = Mallory_hasher.digest()

    Alice_hasher = SHA256.new()
    Alice_hasher.update(Alice_shared_secret)
    alice_key = Alice_hasher.digest()

    Bob_hasher = SHA256.new()
    Bob_hasher.update(Bob_shared_secret)
    bob_key = Bob_hasher.digest()

    # I think the IV is also just the key in this case
    # Cuz if not, not quite sure how mallory gets this value IRL
    iv = get_random_bytes(16)

    print(f"Bob's key {alice_key}\nAlice's key {bob_key}\n")
    Alice_msg = pad(bytes("Hi Bob, i'm Alice", "ascii"), 16)
    print(f"Alice: {unpad(Alice_msg, 16)}")
    Alice_encrypter = AES.new(alice_key, AES.MODE_CBC, iv)   #using alice_key for iv
    Alice_sends_to_Bob = Alice_encrypter.encrypt(Alice_msg)

    Bob_encrypter = AES.new(bob_key, AES.MODE_CBC, iv)       #using bob_key for iv
    Bob_received_from_Alice = Bob_encrypter.decrypt(Alice_sends_to_Bob)
    print(f"Bob received: {unpad(Bob_received_from_Alice, 16)}")

    # Mallory swooping in
    Mallory_encryptor = AES.new(mallory_key, AES.MODE_CBC, iv)
    Mallory_stolen_from_Alice = Mallory_encryptor.decrypt(Alice_sends_to_Bob)
    print(f"Mallory Intercepted: {unpad(Mallory_stolen_from_Alice, 16)}")

if __name__ == "__main__":
    main_1()

def main_2():
    p = 37
    g = 5

    # Get prime for Alice and Bob
    Alice_prime = getPrime(16)
    Bob_prime = getPrime(16)
    print(f"Alice's prime: {Alice_prime}")
    print(f"Bob's prime: {Bob_prime}")

    # Mallory's Modifications
    # g = 1 # This means the public will be 1 & secret will be 1
    # Mallory_stolen_secret = bytes(1)

    # g = p # This means the public and secret will be 0
    # Mallory_stolen_secret = bytes(0)

    g = p - 1 # This means the public and secret will be p - 1
    Mallory_stolen_secret = bytes(p-1) # Ex) (p = 7, g = p-1 = 6, prime=3) => 6^3 % 7 = 6 = (p-1)

    Alice_public = pow(g, Alice_prime) % p
    Bob_public = pow(g, Bob_prime) % p

    Alice_shared_secret = bytes(pow(Bob_public, Alice_prime) % p)
    Bob_shared_secret = bytes(pow(Alice_public, Bob_prime) % p)

    # Mallory can now be sneaky
    Mallory_hasher = SHA256.new()
    Mallory_hasher.update(Mallory_stolen_secret)
    mallory_key = Mallory_hasher.digest()

    Alice_hasher = SHA256.new()
    Alice_hasher.update(Alice_shared_secret)
    alice_key = Alice_hasher.digest()

    Bob_hasher = SHA256.new()
    Bob_hasher.update(Bob_shared_secret)
    bob_key = Bob_hasher.digest()

    # I think the IV is also just the key in this case
    # Cuz if not, not quite sure how mallory gets this value IRL
    iv = get_random_bytes(16)

    print(f"Bob's key {alice_key}\nAlice's key {bob_key}\n")
    Alice_msg = pad(bytes("Hi Bob, i'm Alice", "ascii"), 16)
    print(f"Alice: {unpad(Alice_msg, 16)}")
    Alice_encrypter = AES.new(alice_key, AES.MODE_CBC, iv)   #using alice_key for iv
    Alice_sends_to_Bob = Alice_encrypter.encrypt(Alice_msg)

    Bob_encrypter = AES.new(bob_key, AES.MODE_CBC, iv)       #using bob_key for iv
    Bob_received_from_Alice = Bob_encrypter.decrypt(Alice_sends_to_Bob)
    print(f"Bob received: {unpad(Bob_received_from_Alice, 16)}")

    # Mallory swooping in
    Mallory_encryptor = AES.new(mallory_key, AES.MODE_CBC, iv)
    Mallory_stolen_from_Alice = Mallory_encryptor.decrypt(Alice_sends_to_Bob)
    print(f"Mallory intercepted: {unpad(Mallory_stolen_from_Alice, 16)}")

if __name__ == "__main__":
    main_2()