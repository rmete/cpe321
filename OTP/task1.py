import string
from Cryptodome.Random import get_random_bytes

def xor_strings(s1, s2):
    xor_list = [ord(a) ^ ord(b) for a,b in zip(s1,s2)]
    return "".join('{:02x}'.format(a) for a in xor_list)

def checkStringLengths(s1, s2):
    s1_length = len(s1)
    s2_length = len(s2)
    if s1_length != s2_length:
        return "Error: String lengths don't match.\n String one has length: " + str(s1_length) + "\n String two has length: " + str(s2_length)
    else:
        return xor_strings(s1, s2)


def main():
    s1 = "Darlin dont you go"
    s2 = "and cut your hair!"

    s3 = "Darlin dont you go and"
    s4 = "cut your hair!"

    print ("Test with equal length strings\n\tString1: " + s1 + "\n\tString2: " + s2)
    print (checkStringLengths (s1, s2) + "\n\n")
    print ("Test with non equal length strings\n\tString1: " + s3 + "\n\tString2: " + s4)
    print (checkStringLengths (s3, s4))

if __name__== "__main__":
    main()