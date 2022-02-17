from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
import time


def hash_string(byte_string):
    hasher = SHA256.new()
    hasher.update(byte_string)
    return hasher.digest()


def first_n_bits(input_bytes, n):
    mask = 0xffffffff << (8 - n//8)
    return input_bytes[:n//8] + bytes([input_bytes[n//8] & mask])


def add_1_to_bytes(add1):
    for idx in range(len(add1)):
        added = add1[idx] + 1
        add1[idx] = added % 256
        if added < 256:
            break
    return add1



def find_collision(hash_size_bits):
    start = bytearray(get_random_bytes(hash_size_bits//8 + 1))
    found_hashes = set()
    while True:
        hashed = first_n_bits(hash_string(start), hash_size_bits)
        if hashed in found_hashes:
            break
        found_hashes.add(hashed)
        start = add_1_to_bytes(start)
    return len(found_hashes)



def task1_test_collision_strength():
    with open("test_data.txt", mode="w") as test_data:
        for size in range(8, 51, 2):
            time_to_collide = time.time_ns()
            inputs = find_collision(size)
            time_to_collide = time.time_ns() - time_to_collide
            test_data.write(f"{size}, {inputs}, {time_to_collide}\n")



def main():
    some_strings = ["wow!, look at these words", "there once was an apple?"]
    differ_by_bit = [bytearray(some_strings[0], "ascii") for idx in range(5)]
    for idx in range(len(differ_by_bit)):
        differ_by_bit[idx][idx] = differ_by_bit[idx][idx] ^ (1 << idx)

    print("hashes of some strings")
    for word in some_strings:
        print(hash_string(bytes(word, "ascii")))

    print("hashes of strings which differ by a single bit")
    for word in differ_by_bit:
        print(hash_string(word))

    task1_test_collision_strength()




if __name__ == "__main__":
    main()