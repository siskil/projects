#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>
#include <ctype.h>
#include <string.h>

int j;
int main(int argc, string argv[])

{
    string k = argv[1];
    if(argc == 2)
    {
        for(int i = 0, n = strlen(k); i < n; i++)
        {
            if( (islower(k[i]) || isupper(k[i])) && isdigit(k[i]) == 0 )
            {
                j = 1;
            }
            else
            {
                j = 0;
                break;
                return 1;
            }
        }
        if(j == 1)
            {
                printf("Plaintext: ");
                string p = get_string();
                printf("ciphertext: ");
                for(int i = 0, a = 0, n = strlen(p); i < n; i++)
                {
                    int b = a % strlen(k);
                    if(isalpha(p[i]))
                    {
                        if(islower(p[i]))
                        {
                            char x = (p[i] + (tolower(k[b]) - 97) - 97) % 26;
                            printf("%c", x + 97);
                        }
                        else if(isupper(p[i]))
                        {
                            char x = (p[i] + (tolower(k[b]) - 97) - 65) % 26;
                            printf("%c", x + 65);
                        }
                        a++;
                    }
                    else
                    {
                        printf("%c", p[i]);
                    }
                }
                printf("\n");
                return 0;
            }
            else
            {
                printf("String not accepted.\n");
                return 1;
            }
    }
    else
    {
        printf("Need two arguments!\n");
        return 1;
    }
}