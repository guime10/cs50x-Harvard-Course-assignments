#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>

int main(int argc, char *argv[])
{
    if (argc != 2)
    {
        return 1;
    }

    FILE *raw_file = fopen(argv[1], "r");
    if (raw_file == NULL)
    {
        return 1;
    }

    int BLOCK_SIZE = 512, jpeg = 0;
    typedef uint8_t BYTE;
    BYTE buffer[BLOCK_SIZE];
    char filename[8];
    FILE *img;

    while (fread(buffer, 1, BLOCK_SIZE, raw_file) == BLOCK_SIZE)
    {
        if (buffer[0] == 0xff && buffer[1] == 0xd8 && (buffer[3] & 0xf0) == 0xe0) //verify if is a jpeg
        {
            jpeg++;

            // check first jpeg file
            if (jpeg == 1)
            {
                sprintf(filename, "%03i.jpg", jpeg - 1);
                img = fopen(filename, "w");
            }
            // if jpeg isn't in the first file
            else if (jpeg != 1)
            {
                //closes last file
                fclose(img);

                //save new jpeg
                sprintf(filename, "%03i.jpg", jpeg - 1);
                img = fopen(filename, "w");
            }
        }
        if (jpeg > 0)
        {
            //from buffer to output file
            fwrite(buffer, BLOCK_SIZE, 1, img);
        }
    }
    //close used files
    fclose(img);
    fclose(raw_file);
    return 0;
}