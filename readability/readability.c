#include <cs50.h>
#include <math.h> //round
#include <stdio.h>
#include <string.h>
#include <ctype.h> //isalpha, isspace


int count_letters(string text);
int count_words(string text);
int count_sentences(string text);
float formula(string text);

int main(void)
{
    string text = get_string("Text: ");
    int round_formula = (int) round(formula(text)); //round float to the near int

    if (round_formula > 1 && round_formula < 16)
    {
        printf("Grade %i\n", round_formula);
    }
    else if (round_formula <= 1)
    {
        printf("Before Grade 1\n");
    }
    else
    {
        printf("Grade 16+\n");
    }
}

//count letters
int count_letters(string text)
{
    int count_letters = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char x = text[i];
        if (isalpha(x))
        {
            count_letters++;
        }
    }
    return count_letters;
}

//count words
int count_words(string text)
{
    int count_words = 1;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        char x = text[i];
        if (isspace(x))
        {
            count_words++;
        }
    }
    return count_words;
}

//count sentences
int count_sentences(string text)
{
    int count_sentences = 0;

    for (int i = 0, n = strlen(text); i < n; i++)
    {
        if (text[i] == '!' || text[i] == '.' || text[i] == '?')
        {
            count_sentences++;
        }
    }
    return count_sentences;
}


//Coleman-Liau formula
float formula(string text)
{
    //change to float so it works on the division
    float letters = count_letters(text);
    float words = count_words(text);
    float sentences = count_sentences(text);

    float L = letters / words * 100;
    float S = sentences / words * 100;
    float formula = 0.0588 * L - 0.296 * S - 15.8;
    return formula;
}
