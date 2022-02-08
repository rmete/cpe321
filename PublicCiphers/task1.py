from Crypto.Util.number import getPrime
from Crypto.Hash import SHA256


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

if __name__ == "__main__":
    main()
