from generate import generate
from solve_z3 import solve_z3
from solver_human import solver as human_solver
import argparse
import time

def generate_solvable2(N):
    repr = None
    start = time.perf_counter()
    exclusion = set()
    candidates = 0
    
    while True:
        repr = generate(N, exclusion)
        candidates += 1
        exclusion.add(repr)

        if human_solver() == 1:
            break
    
    end = time.perf_counter()
    total_time = end-start

    return repr, total_time, candidates

def generate_solvable1(N):
    unique_generation_time = 0
    human_solver_time = 0
    repr = None
    total_start = time.perf_counter()
    exclusion = set()
    total_candidates = 0
    unique_candidates = 0


    while True:
        start = time.perf_counter()
        
        while True:    
            repr = generate(N, exclusion)
            total_candidates += 1
            exclusion.add(repr)
            no_of_sols = solve_z3()

            if no_of_sols == 1:
                break
        
        unique_candidates += 1

        end = time.perf_counter()
        unique_generation_time += end - start 

        start = time.perf_counter()
        human_answer = human_solver()
        end = time.perf_counter()
        human_solver_time += end - start

        if human_answer == 1:
            break
    
    total_end = time.perf_counter()
    total_time = total_end - total_start

    return repr, unique_generation_time, human_solver_time, total_time, unique_candidates, total_candidates

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("algo", type=int, help="Which algo to use", choices=(1,2))
    parser.add_argument("N", type=int, help="Size for NxN Box grid")
    
    args = parser.parse_args()

    if args.algo == 1:
        print(generate_solvable1(args.N))
    
    elif args.algo == 2:
        print(generate_solvable2(args.N))
