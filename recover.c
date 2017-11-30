#include <stdio.h>
#include <stdlib.h>
#include <cs50.h>

#define CARD "card.raw"
#define MEMSPC 512

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        fprintf(stderr, "usage: ./recover filename\n");
        return 1;
    }

    char *card = (argc == 2) ? argv[1] : CARD;
    FILE *inptr = fopen(card, "r");

    if(inptr == NULL)
    {
        fprintf(stderr, "Could not open file.");
        return 2;
    }

    unsigned char buffer[MEMSPC];

    int jpgcounter = 0;
    int check = 0;

    FILE *tmp = NULL;

    while(fread(buffer, MEMSPC, 1, inptr))
    {
        if(buffer[0] == 0xff && buffer[1] == 0xd8 && buffer[2] == 0xff && (buffer[3] & 0xf0) == 0xe0)
        {
            if(check != 0)
            {
                fclose (tmp);
            }
            else
            {
                check = 1;
            }

            char name[8];
            sprintf(name, "%03d.jpg", jpgcounter);
            tmp = fopen(name, "a");

            jpgcounter++;
        }

        if (check == 1)
        {
            fwrite(buffer, MEMSPC, 1, tmp);
        }
    }

fclose(inptr);
fclose(tmp);

return 0;
}