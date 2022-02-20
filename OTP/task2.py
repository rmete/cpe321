from Cryptodome.Random import get_random_bytes
import sys
import base64
from Cryptodome.Util.Padding import pad, unpad


def xor_bytes(a, b):
    c = bytearray()
    for idx in range(len(a)):
        c.append(a[idx] ^ b[idx])
    return c


def main(in_file_path): 
    with open(in_file_path, mode='rb') as in_file:
        file_bytes = in_file.read()

    print("THIS IS THE PLAINTEXT:")
    print(file_bytes.decode('utf-8') + "-------------------------------------------\n")
    
    # Get a key of random bytes that is the length of plaintext
    key = get_random_bytes(len(file_bytes))

    # Encrypt a file using OTP 
    with open("encrypt.txt", "wb+") as encrypt:
        encrypt.write(xor_bytes(file_bytes, key))
        encrypt.seek(0)
        encrypt_bytes = encrypt.read()

    print("THIS IS THE ENCRYPTED CIPHERTEXT (not decoded)")
    print(encrypt_bytes) 

    print("\nTHIS IS THE ENCRYPTED CIPHERTEXT (decoded)")
    print(base64.b64encode(encrypt_bytes).decode('utf-8'))
    print("-------------------------------------------\n")

    # Write the decrypted cipher text to a file using the same random key
    # Decode the cipher text so it is in readable format
    with open("decrypt.txt", "w+") as decrypt:
        decrypt.write(xor_bytes(encrypt_bytes, key).decode('utf-8'))
        decrypt.seek(0)
        decrypt_bytes = decrypt.read()

    print("THIS IS THE DECRYPTED CIPHERTEXT:")
    print(decrypt_bytes + "-------------------------------------------\n")

if __name__ == "__main__":
    main(sys.argv[1])