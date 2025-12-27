from generate import generate
from solve_z3 import solve_z3
from solver_human import solver

import argparse
from collections import defaultdict


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("N", type=int, help="Size for NxN Box grid")
    args = parser.parse_args()

    counter = defaultdict(int)
    counter2 = defaultdict(int)

    for i in range(1000):
        generate(args.N)
        counter[solve_z3()] += 1
        counter2[solver()] += 1
        print(i)

    print(counter)
    print(counter2)