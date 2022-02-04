import AES_modes
from Crypto.Random import get_random_bytes
import sys


def main(user_input):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    # when the input is too short there is only one block, so the attack isn't possible
    user_input = "some non-malicious user input, that has at least 256 bytes"
    user_input_bytes = bytes(user_input, "ascii")
    encrypted_bytes = submit(user_input, key, iv)

    #
    #CBC byte flipping attack
    #
    we_want = bytes(";admin=true;____", "ascii")
    decoded_not_xored = AES_modes.xor_bytes(encrypted_bytes[:16], user_input_bytes[16:32]) #second block so we can modify the first
    malicious_cipher_text = AES_modes.xor_bytes(decoded_not_xored, we_want)
    #do modification
    encrypted_bytes = malicious_cipher_text + encrypted_bytes[16:]

    print(verify(encrypted_bytes, key, iv))


def submit(usr_input, key, iv):
    colon = bytes("%3b", "ascii")
    equals = bytes("%3d", "ascii")
    input_bytes = bytearray()
    for char_byte in usr_input:
        if char_byte == ';':
            input_bytes += colon
        elif char_byte == '=':
            input_bytes += equals
        else:
            input_bytes += bytes(char_byte, "ascii")

    input_blocks = AES_modes.get_blocks(input_bytes)
    encrypted = AES_modes.CBC_encrypt(input_blocks, key, iv)
    return encrypted


def verify(input_bytes, key, iv):
    input_blocks = AES_modes.get_blocks(input_bytes)
    decrypted = AES_modes.CBC_decrypt(input_blocks, key, iv)
    print(decrypted)
    look_for = bytes(";admin=true;", "ascii")
    for idx in range(len(look_for) - 1, len(decrypted)):
        if decrypted[idx - len(look_for):idx] == look_for:
            return True
    return False


if __name__ == "__main__":
    main(sys.argv[1])