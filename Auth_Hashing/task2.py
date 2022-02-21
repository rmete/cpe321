from bcrypt import hashpw
from bcrypt import checkpw
from nltk.corpus import words
from time import process_time
import threading


def brute_force(name, hashed_pw, words):
    start = process_time()
    print(f"{name} {hashed_pw}")
    for guess in words:
        if len(guess) > 5 and len(guess) < 11:
            if checkpw(bytes(guess, 'ascii'), bytes(hashed_pw, 'ascii')):
                print(f"{name} found in: {process_time() - start}")
                return


def main():
    threads = []
    name_passwords = []
    with open("shadow.txt", 'r') as to_crack:
        name_passwords = [line.strip().split(':') for line in to_crack.readlines()]

    for line in name_passwords:
        threads.append(threading.Thread(target=brute_force, args=(line[0], line[1], words.words()), daemon=True))
        threads[-1].start()

    for t in threads:
        t.join()

    # thread_alive = True
    # while thread_alive:
    #     thread_alive = False
    #     for t in threads:
    #         if t.is_alive() == True: thread_alive = True

    print("done")





if __name__ == '__main__':
    main()