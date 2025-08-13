#include <cs50.h>
#include <stdio.h>

int main()
{
    int n;
    do
    {
        n = get_int("Length of pyramid: \n");
    }
    while (n < 1);

    for (int i = 0; i < n; i++)
    {
        // printing spaces before hash
        for (int j = 0; j < n - i - 1; j++)
        {
            printf(" ");
        }
        // printing n hashes
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        // printing 2 places
        printf("  ");
        // printing n hashes
        for (int k = 0; k < i + 1; k++)
        {
            printf("#");
        }
        printf("\n");
    }
}
