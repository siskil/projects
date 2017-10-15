#include <stdio.h>
#include <cs50.h>

int i, a, b, c;

int main(void)
{
do  {
    printf("Number of rows = ");
    i = get_int();
    }
while (i < 0 || i > 23);

for (a = 0; a < i; a++) //counts i times
{
    for (b = 0; b < i - a - 1; b++)
    {
    printf(" ");
    }
    for (c = 0; c < a; c++)
    {
    printf("#");
    }

    printf("##" "\n");
}
}