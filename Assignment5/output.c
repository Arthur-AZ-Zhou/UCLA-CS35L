#include "output.h"

bool writeBytes(int nbytes, unsigned long long n) {
    do {
        if (putchar(n) < 0) {
            return false;
        }

        n = n >> CHAR_BIT; //num of characters in bit
        nbytes--;
    } while (nbytes > 0);

  return true;
}

void writeBlock(unsigned long long (*rand64) (void), int blockSize, int nbytes) {
    int result = 0;
    int ind = 0;
    char *outArr = malloc(blockSize * sizeof(char));//we don't actually know size of array, depends on operator

    if (outArr == NULL) {
        fprintf(stderr, "NOTHING TO OUTPUT");
        exit(1);
    }

    while (nbytes > result) {
        unsigned long long tempBlock = rand64(); //get random number
        char temp;

        if (nbytes < blockSize + result) {
            blockSize = nbytes - result;
        }

        while (ind < blockSize && tempBlock > 0) {
            temp = (char) tempBlock;
            outArr[ind] = temp;
            tempBlock = tempBlock >> CHAR_BIT;
            ind++;
        }
        
        if (ind >= blockSize) {
            write(1, outArr, blockSize);
            ind = 0;
            result += blockSize;
        }
    }

    free(outArr); //prevent memory leak
}