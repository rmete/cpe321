import AES_modes
from Crypto.Random import get_random_bytes

def main():
    key = get_random_bytes(16)
    iv = get_random_bytes(16)


def submit(input):
    colon = "%3b"
    equals = "%3d"
    input_bytes = []
    for char_byte in input:
        if char_byte == ';':
            input_bytes.push(colon)
        elif char_byte == '=':
            input_bytes.push(equals)
        else:
            input_bytes.push(char_byte)


if __name__ == "__main__":
    main(sys.argv[1])