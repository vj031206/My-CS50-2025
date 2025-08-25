#include <cs50.h>
#include <stdio.h>

int main()
{
    string name = get_string("What's your name?: "); // inputs name
    printf("hello, %s\n", name);                     // prints hello, and your name
    return 0;
}
