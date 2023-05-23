#include "options.h"

struct options;

void getOption(int argc, char** argv, struct options *chosenOption) {
    // int opt = getopt(argc, argv, "i:o:");
    int opt;
    bool isValid = true;
    int optionNum = 0;

    while ((opt = getopt(argc, argv, "i:o:")) != -1) {
        // opt = getopt(argc, argv, "i:o:");
        switch (opt) {
        case 'i':
            if (optarg[0] != '/' && strcmp(optarg, "rdrand") != 0 && strcmp(optarg, "mrand48_r") != 0) {
                isValid = false;
                break;
            }

            chosenOption->input = optarg;
            optionNum++;
            break;

        case 'o':
            if (strcmp(optarg, "stdio") != 0) {
                char *tailptr;
                int randNum = strtoll(optarg, &tailptr, 10);

                if (*tailptr == '\0' && randNum >= 0) {
                    chosenOption->blockSize = randNum;
                } else {
                    isValid = false;
                }
            }

            optionNum++;
            break;
        }
    }

    if (argc != optionNum * 2 + 2) {
        fprintf(stderr, "BAD ARGUMENTS");
        exit(1);
    } if (optionNum == 0 && argc == 2) {
        char *tailptr;
        errno = 0;
        chosenOption->nbytes = strtoll(argv[1], &tailptr, 10);

        if (errno){
            perror(argv[1]);
        } else {
            isValid = !(*tailptr) && 0 <= chosenOption->nbytes;
        }
    } else if (argc > 2 && argv[optind] != NULL && optionNum != 0) {
      char *tailptr;
      chosenOption->nbytes = strtoll(argv[optind], &tailptr, 10);
    } else {
      isValid = false;
    } if (!isValid) {
      fprintf(stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      exit(1);
    } if (chosenOption->nbytes == 0) {
      exit(0);
    }
}