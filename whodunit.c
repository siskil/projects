#include <stdio.h>
#include <cs50.h>
#include <stdlib.h>

#include "bmp.h"

int main(int argc, char *argv[])
{
    if(argc != 3)
    {
        fprintf(stderr, "Usage: ./whodunit input output");
        return 1;
    }
    else
    {
        char *input = argv[1];
        char *output = argv[2];

        FILE *inptr = fopen(input, "r");
        if(inptr == NULL)
        {
            fprintf(stderr, "%s cannot be opened for reading.", input);
            return 2;
        }

        FILE *outptr = fopen(output, "w");
        if(outptr == NULL)
        {
            fclose (inptr);
            fprintf(stderr, "%s cannot be opened for writing.", output);
            return 3;
        }

        BITMAPFILEHEADER bf;
        fread(&bf, sizeof(BITMAPFILEHEADER), 1, inptr);

        BITMAPINFOHEADER bi;
        fread(&bi, sizeof(BITMAPINFOHEADER), 1, inptr);

        if (bf.bfType != 0x4d42 || bf.bfOffBits != 54 || bi.biSize != 40 || bi.biBitCount != 24 || bi.biCompression != 0)
        {
        fclose(outptr);
        fclose(inptr);
        fprintf(stderr, "Unsupported file format.\n");
        return 4;
        }

        fwrite(&bf, sizeof(BITMAPFILEHEADER), 1, outptr);

        fwrite(&bi, sizeof(BITMAPINFOHEADER), 1, outptr);

        int padding = (4 - (bi.biWidth * sizeof(RGBTRIPLE)) % 4) % 4;

        for(int i = 0, biHeight = abs(bi.biHeight); i < biHeight; i++)
        {
            for(int j = 0; j < bi.biWidth; j++)
            {
                RGBTRIPLE triple;

                fread(&triple, sizeof(RGBTRIPLE), 1, inptr);

                if(triple.rgbtRed == 0xff)
                {
                    triple.rgbtRed = 0x00;
                }

                triple.rgbtBlue = 0x00;
                triple.rgbtGreen = 0x00;

                fwrite(&triple, sizeof(RGBTRIPLE), 1, outptr);
            }
            fseek(inptr, padding, SEEK_CUR);
            for(int k = 0; k < padding; k++)
            {
                fputc(0x00, outptr);
            }
        }
        fclose(inptr);

        fclose(outptr);

        return 0;
    }
}