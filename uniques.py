from generate import generate
from solve_z3 import solve_z3
from solver_human import solver
from utils import save_file

import argparse
from collections import defaultdict


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    # parser.add_argument("N", type=int, help="Size for NxN Box grid")
    # args = parser.parse_args()

    # counter = defaultdict(int)
    # counter2 = defaultdict(int)
    # solutions = set()
    # N = args.N
    
    for N in range(10,11):
        counter = defaultdict(int)
        counter2 = defaultdict(int)
        solutions = set()

        for i in range(1000):
            new_sol = generate(N, solutions, primes=True)
            if i % 100 == 0:
                print(i)

            solutions.add(new_sol)

            z3_solutions = solve_z3()
            human_solver_result = solver()

            counter[z3_solutions] += 1
            counter2[human_solver_result] += 1

            if z3_solutions == 1 and human_solver_result != 1:
                save_file(N)
                
        print(N, counter)
        print(N, counter2)