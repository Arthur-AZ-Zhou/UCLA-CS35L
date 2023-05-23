#ifndef OUTPUT_H
#define OUTPUT_H

#include <limits.h>
#include <stdbool.h>
#include <stdio.h>
#include <unistd.h>
#include <stdlib.h>

bool writeBytes(int nbytes, unsigned long long n);
void writeBlock(unsigned long long (*rand64) (void), int blockSize, int nbytes);

#endif