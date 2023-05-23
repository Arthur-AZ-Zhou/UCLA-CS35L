#ifndef OPTIONS_H
#define OPTIONS_H

#include <errno.h>
#include <stdbool.h>
#include <stdlib.h>
#include <stdio.h>
#include <string.h>
#include <unistd.h>
#include <ctype.h>

struct options {
    int blockSize;
    long long nbytes; //how many bytes to read at one time
    char* input;
};

void getOption(int argc, char **argv, struct options *chosenOption);

#endif