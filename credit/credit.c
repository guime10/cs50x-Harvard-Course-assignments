#include <stdio.h>
#include <cs50.h>

int card_lenght(long card);
int first_digit(long card);
int sum_mult(long card);
int num_mult(long card);
int sum_normal(long card);

int main(void)
{
    //gets card number
    long card = get_long("Credit card number: ");

    //use algorythm to check card number
    int check_card = sum_mult(card) + sum_normal(card);

    //if true check companies
    if (check_card % 10 == 0)
    {

        // CHECK AMEX
        if (first_digit(card) == 34 || first_digit(card) == 37)
        {
            if (card_lenght(card) == 15)
            {
                printf("AMEX\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        //CHECK MASTERCARD
        else if (first_digit(card) > 50 && first_digit(card) < 56)
        {
            if (card_lenght(card) == 16)
            {
                printf("MASTERCARD\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }

        //CHECK VISA
        else if (first_digit(card) / 10 == 4)
        {
            if (card_lenght(card) == 13 || card_lenght(card) == 16)
            {
                printf("VISA\n");
            }
            else
            {
                printf("INVALID\n");
            }
        }
        else
        {
            printf("INVALID\n");
        }
    }
    else
    {
        printf("INVALID\n");
    }
}

//get the card lenght
int card_lenght(long card)
{
    int card_lenght = 0;
    do
    {
        card = card / 10;
        card_lenght++;
    }
    while (card > 0);
    return card_lenght;
}


//gets first card digit
int first_digit(long card)
{
    int first_digit;
    do
    {
        card = card / 10;
        first_digit = card;
    }
    while (card / 100 > 0);
    return first_digit;
}


// adds the numbers multiplied by 2
int sum_mult(long card)
{
    int sum_mult = 0;
    do
    {
        num_mult(card);
        sum_mult = sum_mult + num_mult(card);
        card = card / 100;
    }
    while (card > 0);
    return sum_mult;
}


//gets the numbers to multiply by 2
int num_mult(long card)
{
    card = card / 10; // get the second last to be the last
    int num_mult = (card % 10) * 2; // get the last and * 2
    if (num_mult / 10 > 0) //if the result is > 10
    {
        num_mult = (num_mult % 10) + (num_mult / 10); // it makes num1 + num2
    }
    card = card / 100; //get rid of the number used and the next one
    return num_mult;
}


// gets the numbers not multiplied by 2
int sum_normal(long card)
{
    int sum_normal = 0;
    do
    {
        sum_normal = sum_normal + (card % 10);
        card = card / 100;
    }
    while (card > 0);
    return sum_normal;
}

