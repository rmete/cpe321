from Crypto.Cipher import AES
import sys

def main(file_path):
    cipher = AES.new([key], [mode])
    print("main")

if __name__ == "__main__":
    main(sys.argv[0])