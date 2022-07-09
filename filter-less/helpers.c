#include "helpers.h"
#include <math.h>

//image[i][j].rgbt"color"= 0; (black if everyone is 0)

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    float average = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float total = image[i][j].rgbtRed + image[i][j].rgbtGreen + image[i][j].rgbtBlue;
            average = round((total) / 3);
            image[i][j].rgbtRed = average;
            image[i][j].rgbtGreen = average;
            image[i][j].rgbtBlue = average;
        }
    }
    return;
}

// Convert image to sepia
void sepia(int height, int width, RGBTRIPLE image[height][width])
{
    float sepiaRed = 0, sepiaGreen = 0, sepiaBlue = 0;
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            //sepiaRed = .393 * originalRed + .769 * originalGreen + .189 * originalBlue
            sepiaRed = .393 * image[i][j].rgbtRed + .769 * image[i][j].rgbtGreen + .189 * image[i][j].rgbtBlue;
            sepiaRed = round(sepiaRed);
            if (sepiaRed > 255)
            {
                sepiaRed = 255;
            }
            else if (sepiaRed < 0)
            {
                sepiaRed = 0;
            }

            //sepiaGreen = .349 * originalRed + .686 * originalGreen + .168 * originalBlue
            sepiaGreen = .349 * image[i][j].rgbtRed + .686 * image[i][j].rgbtGreen + .168 * image[i][j].rgbtBlue;
            sepiaGreen = round(sepiaGreen);
            if (sepiaGreen > 255)
            {
                sepiaGreen = 255;
            }
            else if (sepiaGreen < 0)
            {
                sepiaGreen = 0;
            }

            //sepiaBlue = .272 * originalRed + .534 * originalGreen + .131 * originalBlue
            sepiaBlue = .272 * image[i][j].rgbtRed + .534 * image[i][j].rgbtGreen + .131 * image[i][j].rgbtBlue;
            sepiaBlue = round(sepiaBlue);
            if (sepiaBlue > 255)
            {
                sepiaBlue = 255;
            }
            else if (sepiaBlue < 0)
            {
                sepiaBlue = 0;
            }

            image[i][j].rgbtRed = sepiaRed;
            image[i][j].rgbtGreen = sepiaGreen;
            image[i][j].rgbtBlue = sepiaBlue;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width / 2; j++)
        {
            RGBTRIPLE inverter = image[i][j];
            image[i][j] = image[i][width - j - 1];
            image[i][width - j - 1] = inverter;
        }
    }
    return;
}

// Blur image
void blur(int height, int width, RGBTRIPLE image[height][width])
{
    RGBTRIPLE copy[height][width];
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            copy[i][j] = image[i][j];
        }
    }

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            float n = 0, SRed = 0, SGreen = 0, SBlue = 0;
            
            for (int y = i - 1; y <= i + 1; y++) //3 height area scan
            {
                for (int x = j - 1; x <= j + 1; x++) //3 width area scan
                {
                    if (y >= 0 && y < height && x >= 0 && x < width) //checks for corners
                    {
                        SRed += copy[y][x].rgbtRed; //adds all red values
                        SGreen += copy[y][x].rgbtGreen;// adds all green values
                        SBlue += copy[y][x].rgbtBlue;// adds all blue values
                        n++;
                    }
                }
            }
            //AVG results of each color
            image[i][j].rgbtRed = round(SRed / n);
            image[i][j].rgbtGreen = round(SGreen / n);
            image[i][j].rgbtBlue = round(SBlue / n);
        }
    }
    return;
}
