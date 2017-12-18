import cs50

def main():
    while True:
        print("Change owed = ", end="")
        m = cs50.get_float()
        if m > 0:
            break

    m = int(round(m * 100))

    q = 0
    while m >= 25:
        m = m - 25
        q += 1

    a = int(round(m)) % 25

    d = 0
    while a >= 10:
        a = a - 10
        d += 1

    b = int(round(a)) % 10

    n = 0
    while b >= 5:
        b = b - 5
        n += 1

    p = 0
    p = int(round(b)) % 5

    print("Minimum number of coins used is {}".format(q + d + n + p))

if __name__ == "__main__":
    main()
