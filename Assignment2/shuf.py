#! /usr/bin/env python3

import argparse as ap
import random, sys

class shuf:
    def __init__(self, input_lines):
        self.lines = input_lines

    def shuf(self):
        random.shuffle(self.lines)
        for i in range (0, len(self.lines)):
            print(self.lines[i])
    
    def repeat_shuf(self, count = ""):
        if count:
            for _ in range(int(count)):
                print(random.choice(self.lines))
        else:
            while True:
                print(random.choice(self.lines)) 

def main():
    argparser = ap.ArgumentParser()
    argparser.add_argument("input", nargs = "*") #file input
    argparser.add_argument("-e", "--echo", action = "store_true", help = "Treats each command-line operand as an input line.")
    argparser.add_argument("-i", "--input-range", action = "store", help = "Treats each number from LO to HI as input line.")
    argparser.add_argument("-n", "--head-count", action = "store", help = "Outputs at most COUNT lines. By default, all input lines are output.")
    argparser.add_argument("-r", "--repeat", action = "store_true", help = "Repeats output lines.")
    
    argument = argparser.parse_args()
    lines = []

    if argument.echo: # have to be in the front or else argument.input throws file opening error
        lines = argument.input
    elif argument.input: # file input
        if (len(argument.input) == 1):
            try: 
                with open (argument.input[0]) as input_file:
                    for line in input_file.readlines():
                        lines.append(line.strip('\n')) # get rid of whitespaces
            except:
                sys.exit("Invalid input file!")
        else:
            sys.exit("Too many input arguments!")
    elif argument.input_range: # treats range of numbers as input
        try:
            split = argument.input_range.split('-')
            lines = list(range(int(split[0]), int(split[1]) + 1)) # need the +1
        except:
            sys.exit("Invalid input range!")
    else: 
        for line in sys.stdin:
            lines.append(line.strip('\n'))

    s = shuf(lines)
    if argument.repeat:
        s.repeat_shuf(argument.count)
    else:
        s.shuf()  

if __name__ == "__main__":
    main()