#include <cs50.h>
#include <stdio.h>

int main()
{
    // AMEX 15 digits, starts with 34 or 37
    // Mastercard 16 digits, starts with 51, 52, 53, 54, or 55
    // Visa 13 or 16 digits, starts with 4
    long n = get_long("Enter credit card number: \n");
    long num = n; // copy
    int sum = 0, prod, count = 0;
    // checksum
    while (n != 0)
    {
        int digit = n % 10;
        if (count % 2 == 0)
        {
            sum += digit;
        }
        else
        {
            prod = 2 * digit;
            while (prod != 0)
            {
                sum += prod % 10;
                prod /= 10;
            }
        }

        n /= 10;
        count++;
    }

    // identifying provider

    if (sum % 10 == 0)
    {
        long start = num;
        while (start >= 100)
        {
            start /= 10;
        }
        if ((start == 34 || start == 37) && (count == 15))
            printf("AMEX\n");
        else if (((start / 10) == 4) && (count == 13 || count == 16))
            printf("VISA\n");
        else if ((start >= 51 && start <= 55) && (count == 16))
            printf("MASTERCARD\n");
        else
            printf("INVALID\n");
    }
    else
        printf("INVALID\n");
}
