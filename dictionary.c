// Implements a dictionary's functionality

#include "dictionary.h"
#include <ctype.h>
#include <stdbool.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <strings.h>

// Represents a node in a hash table
typedef struct node
{
    char word[LENGTH + 1];
    struct node *next;
} node;

// TODO: Choose number of buckets in hash table
const unsigned int N = 50000;

int num_words = 0;

// Hash table
node *table[N];

// Returns true if word is in dictionary, else false
bool check(const char *input_word)
{
    int index = hash(input_word);
    if (table[index] != NULL)
    {
        node *n = table[index];
        while (n != NULL)
        {
            if (strcasecmp(n->word, input_word) == 0)
                return true;
            else
                n = n->next;
        }
    }
    return false;
}

// Hashes word to a number
unsigned int hash(const char *word)
{
    unsigned long hash = 0;
    for (int i = 0; word[i] != '\0'; i++)
    {
        hash = hash * 31 + toupper(word[i]);
    }
    return hash % N;
}

// Loads dictionary into memory, returning true if successful, else false
bool load(
    const char *dictionary) // loads all of words in dict into data structure, like hash table here
{
    FILE *f = fopen(dictionary, "r");
    if (f == NULL)
        return false;

    char dword[LENGTH + 1]; // word from dictionary
    while (fscanf(f, "%s", dword) == 1)
    {
        int index = hash(dword);
        node *n = malloc(sizeof(node));
        if (n == NULL)
            return false;
        strcpy(n->word, dword);
        n->next = table[index];
        table[index] = n;
        num_words++;
    }

    fclose(f);

    return true;
}

// Returns number of words in dictionary if loaded, else 0 if not yet loaded
unsigned int size(void) //
{
    return num_words;
}

// Unloads dictionary from memory, returning true if successful, else false
bool unload(void)
{
    for (int i = 0; i < N; i++)
    {
        while (table[i] != NULL)
        {
            node *ptr = table[i]->next;
            free(table[i]);
            table[i] = ptr;
        }
    }
    return true;
}
