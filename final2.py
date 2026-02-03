import argparse
import math
import time
from generate import generate
from human_with_hints import hints_solver
from utils import save_file

TRIES_PER_SOLUTION = 3

def final(N, allowed_time=5*60, msgs=False, target_hints=0):
    exclusion = set()
    allowed_hints = math.inf
    start_time = time.perf_counter()

    solution_hints = math.inf
    solution_repr = None

    def terminating_condition():
        return (time.perf_counter() - start_time) >= allowed_time or solution_hints == target_hints

    while not terminating_condition():
        repr = generate(N, exclusion)
        exclusion.add(repr)

        for i in range(TRIES_PER_SOLUTION):
            if terminating_condition():
                break
            
            if msgs:
                print(repr, i)

            human_ans, current_hints = hints_solver(allowed_hints)
            
            if msgs:
                print(human_ans, current_hints)

            if human_ans == 1 and current_hints <= allowed_hints:
                if msgs:
                    print("New minimum!")

                save_file(f"input_{N}", "input.txt", 'w')
                save_file(f"hints_{N}", "hints.txt", 'w')

                solution_hints = current_hints
                solution_repr = repr
                allowed_hints = current_hints - 1
            
    end = time.perf_counter()
    total_time = end-start_time

    return solution_repr, solution_hints, total_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("N", type=int, help="Size for NxN Box grid")

    args = parser.parse_args()

    print(final(args.N, msgs=True))

