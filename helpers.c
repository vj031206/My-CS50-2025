#include "helpers.h"
#include <math.h>
#include <stdio.h>

// Convert image to grayscale
void grayscale(int height, int width, RGBTRIPLE image[height][width])
{
    // navigating to each pixel in 2d array image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double avg = (image[i][j].rgbtBlue + image[i][j].rgbtGreen + image[i][j].rgbtRed) /
                         3.0; // taking average or red, green and blue values
            int r_avg = (int) round(avg);
            image[i][j].rgbtBlue = r_avg;
            image[i][j].rgbtGreen = r_avg;
            image[i][j].rgbtRed = r_avg;
        }
    }
    return;
}

// Reflect image horizontally
void reflect(int height, int width, RGBTRIPLE image[height][width])
{
    for (int i = 0; i < height; i++)
    {
        int start = 0;
        int end = width - 1;
        while (start < end)
        {
            // swap full pixels, not each channel separately
            RGBTRIPLE temp = image[i][start];
            image[i][start] = image[i][end];
            image[i][end] = temp;

            start++;
            end--;
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
            double avg_red = 0;
            double avg_green = 0;
            double avg_blue = 0;
            int counter = 0;

            for (int a = i - 1; a <= i + 1; a++)
            {
                if (a < 0 || a >= height)
                    continue;
                for (int b = j - 1; b <= j + 1; b++)
                {
                    if (b < 0 || b >= width)
                        continue;

                    avg_red += image[a][b].rgbtRed;
                    avg_green += image[a][b].rgbtGreen;
                    avg_blue += image[a][b].rgbtBlue;
                    counter++;
                }
            }

            avg_red /= counter;
            avg_green /= counter;
            avg_blue /= counter;

            copy[i][j].rgbtBlue = (int) round(avg_blue);
            copy[i][j].rgbtGreen = (int) round(avg_green);
            copy[i][j].rgbtRed = (int) round(avg_red);
        }
    }

    // copy blurred image back
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }

    return;
}

// Detect edges
void edges(int height, int width, RGBTRIPLE image[height][width])
{
    // matrix Gx
    int Gx[3][3] = {{-1, 0, 1}, {-2, 0, 2}, {-1, 0, 1}};

    // matrix Gy
    int Gy[3][3] = {{-1, -2, -1}, {0, 0, 0}, {1, 2, 1}};

    RGBTRIPLE copy[height][width];

    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            double Gx_avg_red = 0;
            double Gx_avg_green = 0;
            double Gx_avg_blue = 0;

            double Gy_avg_red = 0;
            double Gy_avg_green = 0;
            double Gy_avg_blue = 0;

            // loop over neighboring pixels
            for (int a = -1; a <= 1; a++)
            {
                for (int b = -1; b <= 1; b++)
                {
                    int x = i + a;
                    int y = j + b;

                    if (x < 0 || x >= height || y < 0 || y >= width)
                        continue;

                    int k = a + 1; // map -1..1 to 0..2
                    int l = b + 1;

                    Gx_avg_red += image[x][y].rgbtRed * Gx[k][l];
                    Gx_avg_green += image[x][y].rgbtGreen * Gx[k][l];
                    Gx_avg_blue += image[x][y].rgbtBlue * Gx[k][l];

                    Gy_avg_red += image[x][y].rgbtRed * Gy[k][l];
                    Gy_avg_green += image[x][y].rgbtGreen * Gy[k][l];
                    Gy_avg_blue += image[x][y].rgbtBlue * Gy[k][l];
                }
            }

            int red = (int) round(sqrt(pow(Gx_avg_red, 2) + pow(Gy_avg_red, 2)));
            int green = (int) round(sqrt(pow(Gx_avg_green, 2) + pow(Gy_avg_green, 2)));
            int blue = (int) round(sqrt(pow(Gx_avg_blue, 2) + pow(Gy_avg_blue, 2)));

            // clamp to 255
            if (red > 255)
                red = 255;
            if (green > 255)
                green = 255;
            if (blue > 255)
                blue = 255;

            copy[i][j].rgbtRed = red;
            copy[i][j].rgbtGreen = green;
            copy[i][j].rgbtBlue = blue;
        }
    }

    // copy results back into image
    for (int i = 0; i < height; i++)
    {
        for (int j = 0; j < width; j++)
        {
            image[i][j] = copy[i][j];
        }
    }

    return;
}
