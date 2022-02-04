import AES_modes
from Crypto.Random import get_random_bytes
import sys

def main(user_input):
    key = get_random_bytes(16)
    iv = get_random_bytes(16)

    encrypted_bytes = submit(user_input, key, iv)
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
    decrypted_str = decrypted.decode("ascii")
    print(decrypted_str)
    look_for = "%3badmin%3dtrue%3b"
    for idx in range(len(look_for) - 1, len(decrypted_str)):
        if decrypted_str[idx - len(look_for):idx] == look_for:
            return True
    return False




if __name__ == "__main__":
    main(sys.argv[1])