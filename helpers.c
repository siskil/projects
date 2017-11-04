/**
 * helpers.c
 *
 * Helper functions for Problem Set 3.
 */

#include <cs50.h>
#include <stdio.h>
#include "helpers.h"

/**
 * Returns true if value is in array of n values, else false.
 */
//void swap(int j, int k);
bool search(int value, int values[], int n)
{
    // TODO: implement a searching algorithm
    int min = 0;
    int max = n - 1;

    if(n < 1)
    {
        return false;
    }
    else
    {
        while(min <= max)
        {
            int mid = (min + max) / 2;
            if(value == values[mid])
            {
                return true;
            }
            else if(value < values[mid])
            {
                max = mid - 1;
            }
            else if(value > values[mid])
            {
                min = mid + 1;
            }
        }
        return false;
    }
}

/**
 * Sorts array of n values.
 */

void sort(int values[], int n)
{
    // TODO: implement a sorting algorithm
    for(int i = 0; i < n - 1; i++)
    {
        for(int j = 0; j < n - i - 1; j++)
        {
            if(values[j] > values[j + 1])
            {
                int tmp = values[j];
                values[j] = values[j + 1];
                values[j + 1] = tmp;
            }
        }
    }
}

