#include <cs50.h>
#include <ctype.h>
#include <stdio.h>
#include <string.h>

int scrabble(string s); // function prototype

int main(void)
{
    string word1 = get_string("Player 1: \n");
    string word2 = get_string("Player 2: \n");
    int score1 = scrabble(word1), score2 = scrabble(word2); // assigning scores for each player

    // comparing scores
    if (score1 > score2)
        printf("Player 1 wins!\n");
    else if (score1 < score2)
        printf("Player 2 wins!\n");
    else
        printf("Tie!\n");
}

// function for calculation scrabble score for a given word
int scrabble(string s)
{
    int score = 0;
    int points[] = {1, 3, 3, 2, 1, 4, 2, 4, 1, 8, 5, 1, 3, 1, 1, 3, 10, 1, 1, 1, 1, 4, 4, 8, 4, 10};
    // looping through each letter of the word
    for (int i = 0, n = strlen(s); i < n; i++)
    {
        // checks if char is an alphabet, only then proceeds
        if (isalpha(s[i]))
        {
            int letter_index = toupper(s[i]) - 'A';
            score += points[letter_index];
        }
    }
    return score; // returning the score value
}
