#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

// declaring a byte
typedef uint8_t BYTE;

void recover(FILE *f);

int main(int argc, char *argv[])
{
    // checking if only one command like argument is passed
    if (argc != 2)
    {
        printf("Usage: ./recover filename.jpeg");
        return 1;
    }

    // opening a file f
    FILE *f = fopen(argv[1], "r");
    if (f == NULL)
    {
        printf("Could not open file.\n");
        return 1;
    }

    recover(f); // recovering the jpegs from file f
    fclose(f);  // closing the file f after recovery is complete
}

void recover(FILE *f)
{
    // count set to -1 so that filenames start from 000.jpeg
    int jpg_count = -1;

    // allocating 512 bytes to pointer b
    BYTE *b = malloc(512 * sizeof(BYTE));
    if (b == NULL)
    {
        printf("Memory allocation failed\n");
        return;
    }
    // filename is 8 character, including NUL at the end
    char fileout[8];
    // declaring jpeg file initially
    FILE *jpgout = NULL;
    while (fread(b, sizeof(BYTE), 512, f) == 512)
    {
        if ((b[0] == 0xff) && (b[1] == 0xd8) && (b[2] == 0xff) && ((b[3] & 0xf0) == 0xe0))
        {
            if (jpgout != NULL)
                // closing file before opening a new file once new signature seen
                fclose(jpgout);
            // counting no of jpegs in the file
            jpg_count++;
            // naming file as ###.jpg where it starts from 000.jpg
            sprintf(fileout, "%03i.jpg", jpg_count);
            // opening a new file if jpg signature seen
            jpgout = fopen(fileout, "w");
        }

        if (jpgout != NULL)
            // to avoid segmentation error
            fwrite(b, sizeof(BYTE), 512, jpgout);
    }

    if (jpgout != NULL)
        fclose(jpgout); // explicityly closes the jpg files

    free(b); // frees the memory allocated for b
}
