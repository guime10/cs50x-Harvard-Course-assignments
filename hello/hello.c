#include <stdio.h>
#include <cs50.h>

int main(void)
{
    //get the user name
    string name = get_string("What is your name? ");
    //print hello to the user
    printf("Hello, %s!\n", name);
}