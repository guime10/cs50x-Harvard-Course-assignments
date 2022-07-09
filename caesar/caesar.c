#include <cs50.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <ctype.h>

int main(int argc, string argv[])
{
    // gets only one string
    if (argc != 2)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    //get user text
    string text = get_string("Text: ");

    //makes argv an char and makes it an int
    int key = atoi(argv[1]);
    if (key < 0)
    {
        printf("Usage: ./caesar key\n");
        return 1;
    }

    printf("ciphertext: ");
    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char x = text[i];
        //if is not alpha
        if (!isalpha(x))
        {
            printf("%c", x);
        }
        else
        {
            //if letter is lowcase
            if (islower(x))
            {
                printf("%c", (x - 97 + key) % 26 + 97);
            }
            //is letter is uppercase
            else if (isupper(x))
            {
                printf("%c", (x - 65 + key) % 26 + 65);
            }
        }
    }
    printf("\n");
}