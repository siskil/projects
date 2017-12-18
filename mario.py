import cs50

def main():
    while True:
        print("i = ", end="")
        i = cs50.get_int()
        if i > 0 or i < 23:
            break

    for a in range(i):
        for b in range(i - a - 1):
            print(" ", end="")
        for c in range(a):
            print("#", end="")
        print("##")

if __name__ == "__main__":
    main()