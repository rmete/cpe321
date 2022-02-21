from Cryptodome.Random import get_random_bytes
from sys import *


def xor_bytes(a, b):
    c = bytearray()
    for idx in range(len(a)):
        c.append(a[idx] ^ b[idx])
    return c

def write_file(outfile, header, ciphertext):
    # Write to output file, for this we need the original bmp header 
    # and the encrypted ciphertext
    with open(outfile, 'wb') as output:
        output.write(header+ciphertext)


def main(): 

    in_file_path1 = argv[1]
    in_file_path2 = argv[2]

    print(in_file_path2)
    with open(in_file_path1, mode='rb') as plaintext1:
        plaintext1 = plaintext1.read()


    with open(in_file_path2, mode='rb') as plaintext2:
        plaintext2 = plaintext2.read()

    # Preserve header and get bytes for the image
    header1 = plaintext1[:54]
    image1 = plaintext1[54:]
    header2 = plaintext2[:54]
    image2 = plaintext2[54:]
    
    # Get a key of random bytes that is the length of plaintext
    # This key will be used for both image encryptions 
    key = get_random_bytes(len(image2))

    # Get the encrypted ciphertext for both images
    # Use the same key to encrypt both
    ciphertext1 = xor_bytes(image1, key)
    ciphertext2 = xor_bytes(image2, key)

    # XOR both encrypted images together
    decrypted_ciphertext = xor_bytes(ciphertext1, ciphertext2)

    # Write the encrypted images to a file
    encrypted_file1 = in_file_path1.split(".")[0] + "_two_time_pad_encrypted.bmp"
    write_file(encrypted_file1, header1, ciphertext1)
    encrypted_file2 = in_file_path2.split(".")[0] + "_two_time_pad_encrypted.bmp"
    write_file(encrypted_file2, header2, ciphertext2)

    # Write the decrypted image to a bmp file
    decrypted_file1 = in_file_path1.split(".")[0] + "_two_time_pad_decrypted.bmp"
    write_file(decrypted_file1, header1, decrypted_ciphertext)

    # Write the decrypted image to a bmp file
    decrypted_file2 = in_file_path2.split(".")[0] + "_two_time_pad_decrypted.bmp"
    write_file(decrypted_file2, header2, decrypted_ciphertext)

if __name__ == "__main__":
    main()