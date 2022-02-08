from Crypto.Cipher import AES
import sys
from Crypto.Random import get_random_bytes


def main(infile):
    #infile = sys.argv[1]
    with open(infile, 'rb') as input:
        plaintext = input.read()

    # Preserve header and get bytes for the image
    header = plaintext[:54]
    image = plaintext[54:]

    # Break up image into 16 byte block
    blocks = get_blocks(image)

    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # Encrypt with ebc and cbc method
    ebc_out_bytes = EBC_encrypt(blocks)
    cbc_out_bytes = CBC_encrypt(blocks, key, iv)

    encrypted_blocks = get_blocks(cbc_out_bytes)

    # Decrypt with cbc method
    cbc_decrypt = CBC_decrypt(encrypted_blocks, key, iv)

    # Write ebc encrypted file
    outfile_ebc = infile.split(".")[0] + "_ebc.bmp"
    write_file(outfile_ebc, header, ebc_out_bytes)

    # Write cbc encrypted file
    outfile_cbc = infile.split(".")[0] + "_cbc.bmp"
    write_file(outfile_cbc, header, cbc_out_bytes)

    # Write cbc decrypted file
    outfile_cbc_decypted = infile.split(".")[0] + "_decrypted_cbc.bmp"
    write_file(outfile_cbc_decypted, header, cbc_decrypt)

    

def pkcs7_pad(to_pad, m):
    if len(to_pad) % m != 0:
        pad_with = (m * (len(to_pad) // m + 1)) - len(to_pad)
        to_pad = to_pad + bytes([pad_with] * pad_with)
    return to_pad

def get_blocks(file_as_bytes):
    file_as_bytes = pkcs7_pad(file_as_bytes, 16)
    blocks = [bytes(file_as_bytes[x - 16: x]) for x in range(16, len(file_as_bytes) + 1, 16)]
    return blocks

def EBC_encrypt(blocks):
    ciphertext = b""
    random_key = get_random_bytes(16)
    ecb_cipher = AES.new(random_key, AES.MODE_ECB)

    # loop through blocks and encrypt each block independently 
    for block in blocks:
        ciphertext += ecb_cipher.encrypt(block)
    
    return ciphertext

def xor_bytes(a, b):
    c = bytearray()
    for idx in range(16):
        c.append(a[idx] ^ b[idx])
    return c

def CBC_encrypt(blocks, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    encrypted = bytearray()
    for bytes_16 in blocks:
        intermediate = xor_bytes(iv, bytes_16)
        iv = cipher.encrypt(intermediate)
        encrypted += iv
    return encrypted

def CBC_decrypt(blocks, key, iv):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = bytearray()
    for bytes_16 in blocks:
        intermediate = cipher.decrypt(bytes_16)
        decrypted += xor_bytes(iv, intermediate)
        iv = bytes_16
    return decrypted

def write_file(outfile, header, ciphertext):
    # Write to output file, for this we need the original bmp header 
    # and the encrypted ciphertext
    with open(outfile, "wb") as output:
        output.write(header+ciphertext)

if __name__ == "__main__":
    main(sys.argv[1])