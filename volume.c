// Modifies the volume of an audio file

#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// Number of bytes in .wav header
const int HEADER_SIZE = 44;

typedef uint8_t BYTE;   // declaring byte data type containing 1 byte each
typedef int16_t SAMPLE; // declaring sample data type containing 2 bytes each

int main(int argc, char *argv[])
{
    // Check command-line arguments
    if (argc != 4)
    {
        printf("Usage: ./volume input.wav output.wav factor\n");
        return 1;
    }

    // Open files and determine scaling factor
    FILE *input = fopen(argv[1], "r");
    if (input == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    FILE *output = fopen(argv[2], "w");
    if (output == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    float factor = atof(argv[3]);

    // TODO: Copy header from input file to output file
    BYTE b;
    int counter = 0;

    while (fread(&b, sizeof(b), 1, input) != 0)
    {
        counter += 1; // incrementing counter
        fwrite(&b, sizeof(b), 1, output);
        if (counter == HEADER_SIZE) // if counter equals header size, loop ends
            break;
    }

    // TODO: Read samples from input file and write updated data to output file
    SAMPLE s;

    fseek(input, HEADER_SIZE, SEEK_SET); // pointing cursor at index HEADER_SIZE from beginning
    while (fread(&s, sizeof(s), 1, input) != 0)
    {
        s *= factor;                        // multiplying sample by factor
        (fwrite(&s, sizeof(s), 1, output)); // writing sample to output
    }

    // Close files
    fclose(input);
    fclose(output);
}
