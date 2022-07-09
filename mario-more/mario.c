#include <cs50.h>
#include <stdio.h>

int main (void)
{
    int height;

    do
    {
        height = get_int("Heigth: ");
    }
    while (height < 1 || height > 8);


    //for each roll
    for (int i = 0; i < height ; i++)
    {
        //make spaces
        for (int space = height - 1; space > i; space--)
        {
            printf(" ");
        }

        //make left hashes
        for (int j = 0 ; j <= i ; j++)
        {
            //print brick
            printf("#");
        }
        //^^^ correct ^^^

        // make middle spaces
        printf("  ");

        //make right hashes
        for (int j = 0 ; j <= i ; j++)
        {
            //print brick
            printf("#");
        }
        printf("\n");
    }
}