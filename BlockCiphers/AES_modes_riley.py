from Crypto.Cipher import AES
import sys
from os import urandom


def main():
    infile = sys.argv[1]
    with open(infile, 'rb') as input:
        plaintext = input.read()
    header = plaintext[:54]
    image = plaintext[54:]
    blocks = get_blocks(image)
    EBC_encrypt(infile, blocks, header)

# Breakup plaintext into blocks of length 16
# Pad last block if needed with 0s and 1s
def get_blocks(plaintext):
    blocks = []
    for i in range(0, len(plaintext), 16):
        block = plaintext[i : i + 16]
        if (len(block) < 16):
            for j in range(16 - len(block)):
                block + "0" if j % 2 == 0 else "1"
        blocks.append(block)
    return blocks

def EBC_encrypt(infile, blocks, header):
    # get the name of file without extension and 
    outfile = infile.split(".")[0] + "_ebc.bmp"
    ciphertext = b""
    random_key = urandom(16)
    ecb_cipher = AES.new(random_key)

    # loop through blocks and encrypt each block independently 
    for block in blocks:
        ciphertext += ecb_cipher.encrypt(block)

    # Write to output file, for this we need the original bmp header 
    # and the encrypted ciphertext
    with open(outfile, "wb") as output:
        output.write(header+ciphertext)


if __name__ == "__main__":
    main(sys.argv[0])