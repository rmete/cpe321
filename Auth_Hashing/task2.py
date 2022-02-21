from bcrypt import hashpw
from bcrypt import checkpw
from nltk.corpus import words
from time import process_time
import threading


def brute_force(name, hashed_pw):
    start = process_time()
    for guess in words:
        if checkpw(guess, hashed_pw):
            print(f"{name} found in: {process_time() - start}")
            return


def main():
    threads = []
    with open("shadow.txt", 'rb') as to_crack:
        line = to_crack.readline().split(':')
        print(line)
        threads.append(threading.Thread(brute_force, (line[0], line[1])))
        threads[-1].run()




if __name__ == '__main__':
    main()