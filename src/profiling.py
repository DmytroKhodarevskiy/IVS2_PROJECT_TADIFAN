#!/usr/bin/env python
import sys
import os


# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
# sys.path.insert(0, parent_dir)

# Get the directory of the current script
current_dir = os.path.dirname(__file__)

# Go up one level from the current directory
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))

# Add the parent directory to the system path
sys.path.insert(0, parent_dir)

#from src import Calc_Library
#If you have the script inside th src folder, you can use the line below instead of the previous one
#If you have profiling inside the profiling folder, you can use the line above
import Calc_Library

#data.txt must be in the same folder as the script, which contains numbers followed by newlines
#For running the program use the command: 'python profiling.py data.txt'
#For visualisation information about profiling the program use: 'python -m cProfile profiling.py data.txt'
#In file data.txt must be numbers

def samplemean(numbers):
    return summs(numbers) / len(numbers)
def summs(numbers):
    summ = 0
    for n in numbers:
        summ = Calc_Library.Plus(summ, n)
    return summ

def stddev(numbers):
        x_sample = samplemean(numbers)
        minus = [Calc_Library.Minus(x, x_sample) for x in numbers]
        sqrt = [Calc_Library.Power(d, 2) for d in minus]
        sum_squares = summs(sqrt)
        N = len(numbers)
        befsq = Calc_Library.Divide(sum_squares, N)
        s = Calc_Library.SquareRoot(befsq)
        return s



def main():
    if len(sys.argv) < 2:
        print("Error: Input file not specified")
        return
    filename = sys.argv[1]
    with open(filename, "r") as f:
        data = f.read()
        numbers = [float(x) for x in data.split()]
    result = stddev(numbers)
    print("sd =",result)
if __name__ == "__main__":
    main()
