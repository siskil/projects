#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <string.h>
#include <ctype.h>

int main(int argc, string argv[])

{
    if(argc != 2)
    {
        printf("Invalid input!\n");
        return 1;
    }
    else
    {
        int i = atoi(argv[1]);

        printf("Plaintext: ");
        string p = get_string();

        printf("Ciphertext: ");

        for(int j = 0, n = strlen(p); j < n; j++)
        {
            if( isalpha(p[j]) != 0 )
            {
                if (p[j] >= 'a' && p[j] <= 'z')
                {
                    char x = ((p[j] + i) - 97) % 26;
                    printf("%c", x + 97);
                }
                if (p[j] >= 'A' && p[j] <= 'Z')
                {
                    char x = ((p[j] + i) - 65) % 26;
                    printf("%c", x + 65);
                }
            }
            else
            {
                printf("%c", p[j]);
            }
        }
        printf("\n");
        return 0;
    }
}