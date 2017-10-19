#include <stdio.h>
#include <cs50.h>
#include <math.h>

float m, a, b;
int q, d, n, p;

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
m = (round) (m);

{printf("m = %f\n", m);}
while (m >= 25)
{
    m = m - 25;
    q++;
}
{printf("q = %i\n", q);}
a = (int) (m) % 25;

while (a >= 10)
{
	a = a - 10;
	d++;
}
{printf("d = %i\n", d);}
b = (int) (a) % 10;

while (b >= 5)
{
	b = b - 5;
	n++;
}
{printf("n = %i\n", n);}

p = (int) (b) % 5;

{printf("p = %i\n", p);}
{
    printf("Minimum number of coins used is %i\n", q + d + n + p);
}

}