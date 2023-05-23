/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */
#include "options.h"
#include "output.h"
#include "rand64-hw.h"
#include "rand64-sw.h"

/* Main program, which outputs N bytes of random data.  */
int main(int argc, char **argv) {
    /* Check arguments.  */
    struct options option;
    option.nbytes = 0;
     option.input = "rdrand";
    option.blockSize = -1;
    char *file = "/dev/random";

    getOption(argc, argv, &option);

    /* Now that we know we have work to do, arrange to use the appropriate library.  */
    void (*inititalize) (void);
    unsigned long long (*rand64) (void);
    void (*finalize) (void);
    bool canInit = true;

    if (strcmp(option.input, "rdand") == 0) {
        if (rdrand_supported()) {
            inititalize = hardware_rand64_init;
            rand64 = hardware_rand64;
            finalize = hardware_rand64_fini;
        } else {
            return 1;
        }
    } else if (strcmp(option.input, "mrand48_r") == 0) {
        inititalize = mrand48_init;
        rand64 = mrand48_rng;
        finalize = mrand48_fini;
    } else {
        if (option.input[0] == '/') {
            file = option.input;
        }

        software_rand64_init(file);
        rand64 = software_rand64;
        finalize = software_rand64_fini;
        canInit = false;
    }

    if (canInit) {
        inititalize();
    }

    int wordSize = sizeof rand64();
    int outputErrno = 0;
    long long nbytes = option.nbytes;

    //normal output
    if (option.blockSize == -1) {
        do {
            unsigned long long n = rand64();
            int outbytes = (nbytes < wordSize)? nbytes : wordSize;
            if (!writeBytes(outbytes, n)) {
                outputErrno = errno;
                break;
            }
            nbytes -= outbytes;
        } while (0 < nbytes);
    } else {
        writeBlock(rand64, option.blockSize, option.nbytes);
    }

    if (fclose(stdout) != 0) {
        outputErrno = errno;
    }

    if (outputErrno) {
        errno = outputErrno;
        perror("output");
    }

    finalize();
    return !!outputErrno; //return 1 or 0
}

// int main(int argc, char **argv)
// {
//   /* Check arguments.  */
//   struct options option;
//   option.nbytes = 0;
//   option.input = "rdrand";
//   option.blockSize = -1;
//   getOption(argc, argv, &option);

//   char *file = "/dev/random";

//   /* Now that we know we have work to do, arrange to use the
//      appropriate library.  */
//   void (*initialize)(void);
//   unsigned long long (*rand64)(void);
//   void (*finalize)(void);
//   bool canInitialize = true;
//   if (strcmp(option.input, "rdand") == 0)
//   {
//     if (rdrand_supported())
//     {
//       initialize = hardware_rand64_init;
//       rand64 = hardware_rand64;
//       finalize = hardware_rand64_fini;
//     }
//     else
//       return 1;
//   }
//   else if (strcmp(option.input, "mrand48_r") == 0)
//   {
//     initialize = mrand48_init;
//     rand64 = mrand48_rng;
//     finalize = mrand48_fini;
//   }
//   else
//   {
//     if (option.input[0] == '/')
//     {
//       file = option.input;
//     }
//     software_rand64_init(file);
//     canInitialize = false;
//     rand64 = software_rand64;
//     finalize = software_rand64_fini;
//   }
//   if (canInitialize)
//   {
//     initialize();
//   }

//   int wordsize = sizeof rand64();
//   int output_errno = 0;
//   long long nbytes = option.nbytes;

//   // output as normal
//   if (option.blockSize == -1)
//   {
//     do
//     {
//       unsigned long long x = rand64();
//       int outbytes = nbytes < wordsize ? nbytes : wordsize;
//       if (!writeBytes(x, outbytes))
//       {
//         output_errno = errno;
//         break;
//       }
//       nbytes -= outbytes;
//     } while (0 < nbytes);
//   }
//   else
//   {
//     writeBlock(rand64, option.blockSize, option.nbytes);
//   }

//   if (fclose(stdout) != 0)
//     output_errno = errno;

//   if (output_errno)
//   {
//     errno = output_errno;
//     perror("output");
//   }
//   finalize();
//   return !!output_errno;
// }