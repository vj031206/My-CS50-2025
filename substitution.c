#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int keychecker(string key);

int main(int argc, string argv[])
{
    if ((argc == 2) && (keychecker(argv[1]))) // checks for correct input and key
    {
        string plain = get_string("plaintext: ");
        int length = strlen(plain);
        char cipher[length];

        for (int i = 0; i < length; i++)
        {
            if (isupper(plain[i])) // replacing uppercase letters
            {
                int letter_index = plain[i] - 'A';
                cipher[i] = toupper(argv[1][letter_index]);
            }
            else if (islower(plain[i])) // replacing lowercase letters
            {
                int letter_index = plain[i] - 'a';
                cipher[i] = tolower(argv[1][letter_index]);
            }
            else
                cipher[i] = plain[i];
        }
        printf("ciphertext: ");
        for (int i = 0; i < length; i++)
            printf("%c", cipher[i]);
        printf("\n");
    }

    else // in case of invalid key or input in command line
    {
        printf("Key must contain 26 characters.\n");
        return 1;
    }
    return 0;
}

// checking for validity of key
int keychecker(string key)
{
    int n = strlen(key);
    int no_alpha = 26;
    if (n != no_alpha) // checks if key has 26 characters
        return 0;

    for (int i = 0; i < n; i++)
    {
        if (!(isalpha(key[i]))) // checks if all letters in key are alphabets only
            return 0;
        else // checks for duplication
            for (int j = i + 1; j < n; j++)
            {
                if (tolower(key[i]) == tolower(key[j]))
                    return 0;
            }
    }
    return 1; // key is valid
}
