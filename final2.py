import argparse
import math
import time
from generate import generate
from human_with_hints import hints_solver
from utils import save_file

TRIES_PER_SOLUTION = 5

def final(N, allowed_time=5*60, msgs=False, target_hints=0, allowed_iterations=math.inf):
    exclusion = set()
    allowed_hints = math.inf
    start_time = time.perf_counter()
    iterations = 0

    solution_hints = math.inf
    solution_repr = None

    def terminating_condition():
        return (time.perf_counter() - start_time) >= allowed_time or solution_hints == target_hints or iterations == allowed_iterations

    while not terminating_condition():
        repr = generate(N, exclusion)
        exclusion.add(repr)

        for i in range(TRIES_PER_SOLUTION):
            iterations += 1
            if terminating_condition():
                break
            
            if msgs:
                print(repr, i)

            human_ans, current_hints = hints_solver(allowed_hints)
            
            with open('experiment2.txt', 'a') as file:
                file.write(f"{repr} {i} {human_ans} {current_hints}\n")

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

    return solution_repr, solution_hints, total_time, iterations

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("N", type=int, help="Size for NxN Box grid")

    args = parser.parse_args()

    final(15, allowed_time=math.inf, msgs=True,allowed_iterations=1000)

    # print(final(args.N, msgs=True))

