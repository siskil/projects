import cs50
import sys

def main():

    if len(sys.argv) != 2:
        print ("usage: python vigenere.py key")
    else:
        key = sys.argv[1]

        if sys.argv[1].isalpha() == False:
            exit(1)
        else:
            print ("plaintext: ", end="")
            plain = cs50.get_string()
            print ("cyphertext: ", end="")
            a = 0

            for j in plain:
                if j.isalpha():
                    k = sys.argv[1][a]
                    if j.islower():
                        x = (((ord(j) - 97) + (ord(k.lower()) - 97)) % 26) + 97
                        print ("{}".format(chr(x)), end="")

                    elif j.isupper():
                        x = (((ord(j) - 65) + (ord(k.lower()) - 97)) % 26) + 65
                        print ("{}".format(chr(x)), end="")

                    a += 1
                    a = (a + len(key)) % len(key)

                else:
                    print ("{}".format(j), end="")

            print("\n", end="")

if __name__ == "__main__":
    main()


