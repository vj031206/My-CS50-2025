#include <cs50.h>
#include <ctype.h>
#include <math.h>
#include <stdio.h>
#include <string.h>

double grader(string s); // function prototype

int main(void)
{
    string text = get_string("Text: \n"); // accepts string from user
    double grade = round(grader(text));   // rounding of grade to nearest whole number

    // grade conditionals
    if (grade < 1)
        printf("Before Grade 1\n");
    else if (grade > 16)
        printf("Grade 16+\n");
    else
        printf("Grade %i\n", (int) grade);
}

double grader(string txt)
{
    float letters = 0, sentences = 0, words = 1; // float because int divided by int gives int

    // counting no of letters, words and sentences
    for (int i = 0, n = strlen(txt); i < n; i++)
    {
        if (isalnum(txt[i]))
            letters++;
        else if ((txt[i] == '.') || (txt[i] == '!') || (txt[i] == '?'))
            sentences++;
        else if (isspace(txt[i]))
            words++;
    }

    // calculating grade
    float l = (letters / words) * 100;
    float s = (sentences / words) * 100;
    double index = 0.0588 * l - 0.296 * s - 15.8;

    return index;
}
