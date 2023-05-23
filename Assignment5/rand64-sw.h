#ifndef RAND64_SW_H
#define RAND64_SW_H

#include <limits.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>
#include <time.h>

void software_rand64_init (char* file);
unsigned long long software_rand64 (void);
void software_rand64_fini (void);

void mrand48_init(void);
unsigned long long mrand48_rng(void);
void mrand48_fini(void);

#endif