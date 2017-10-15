#include <stdio.h>
#include <cs50.h>

float m, a, b, c;
int q, d, n, p, x, y;
int main(void)

{
    do
    {
    printf("Change owed = ");
    m = get_float();
    }
while
    (m <= 0);

m = m * 100;

a = m / 25;

    if (a > 1)
    {
    q = (int) a;
    }
    else
    {
    (q = 0);
    }

x = (int) (m) % 25;
b = x / 10;

    if (b > 1)
    {
    d = (int) b;
    }
    else
    {
    (d = 0);
    }

y = x % 10;
c = y / 5;

    if (c > 1)
    {
    n = (int) c;
    }
    else
    {
    (c = 0);
    }
p = y % 5;

{
    printf("Minimum number of coins used is %i\n", q + d + n + p);
}

}
