from Cryptodome.Random import get_random_bytes
import sys


def xor_bytes(a, b):
    c = bytearray()
    for idx in range(len(a)):
        c.append(a[idx] ^ b[idx])
    return c

def write_file(outfile, header, ciphertext):
    # Write to output file, for this we need the original bmp header 
    # and the encrypted ciphertext
    with open(outfile, "wb") as output:
        output.write(header+ciphertext)


def main(in_file_path): 
    with open(in_file_path, mode='rb') as plaintext:
        plaintext = plaintext.read()

    # Preserve header and get bytes for the image
    header = plaintext[:54]
    image = plaintext[54:]
    
    # Get a key of random bytes that is the length of plaintext
    key = get_random_bytes(len(image))

    ciphertext = xor_bytes(image, key)

    # Encrypt a BMP image using OTP
    encrypted_file = in_file_path.split(".")[0] + "_otp_encrypted.bmp"
    write_file(encrypted_file, header, ciphertext)

    # Decrypt a BMP image using the same key used in OTP encryption
    decrypted_ciphertext = xor_bytes(ciphertext, key)

    # Write the decrypted image to a bmp file
    decrypted_file = in_file_path.split(".")[0] + "_otp_decrypted.bmp"
    write_file(decrypted_file, header, decrypted_ciphertext)

if __name__ == "__main__":
    main(sys.argv[1])