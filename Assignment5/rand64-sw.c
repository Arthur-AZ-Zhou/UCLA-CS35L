#include "rand64-sw.h"

/* Input stream containing random bytes.  */
FILE *urandstream;

/* Initialize the software rand64 implementation.  */
void software_rand64_init (char* readfile) {
  urandstream = fopen (readfile, "r");
  if (! urandstream) {
    abort ();
  }
}

/* Return a random value, using software operations.  */
unsigned long long software_rand64 (void) {
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void software_rand64_fini(void) {
  fclose(urandstream);
}

void mrand48_init(void) {}

unsigned long long mrand48_rng(void) {
  unsigned long long returnNum = 0;
  struct drand48_data buffer;

  srand48_r(time(NULL), &buffer); //make mrand seed based on current time
  mrand48_r(&buffer, (long int *) &returnNum);
  return returnNum;
}

void mrand48_fini(void) {}
