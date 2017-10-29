#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <ctype.h>

int main(void)

{
    //printf("Please input name : ");
    string name = get_string();
    if (name != NULL)

    for (int i = 0, n = strlen(name); i < n; i++)
    {
        if ( (isblank(name[i - 1]) || isalpha(name[i - 1]) == 0) && isalpha(name[i]) )
        {
            printf("%c", toupper(name[i]));
        }
    }
    printf("\n");

}


