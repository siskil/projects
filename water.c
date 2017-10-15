#include <stdio.h>
#include <cs50.h>

int i;
int main(void)

{
    printf("Shower time = ");
    i = get_int();
    printf("Number of used water bottles is %i\n", i * 12);
}