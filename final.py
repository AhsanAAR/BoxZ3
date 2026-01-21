from generate import generate
from solve_z3 import solve_z3
from human_with_hints import hints_solver as human_solver
import argparse
import time

def final(N, check_unique, max_iterations=10, hints_start=0, msgs=False):
    allowed_hints = hints_start
    exclusion = set()
    repr = None

    start = time.perf_counter()

    while True:
        human_ans = -1

        for i in range(max_iterations):
            repr = generate(N, exclusion)
            exclusion.add(repr)
            
            if check_unique:
                while True:
                    no_of_sols = solve_z3()
                    if no_of_sols == 1:
                        break
                    
                    repr = generate(N, exclusion)
                    exclusion.add(repr)

            human_ans, used_hints = human_solver(allowed_hints)

            if msgs:
                print(allowed_hints, i, repr, human_ans, used_hints)
 
            if human_ans == 1:
                break
        
        if human_ans == 1:
            break
        
        allowed_hints += 1
        
        if msgs:
            print("Hints: ", allowed_hints)
    
    end = time.perf_counter()
    total_time = end-start

    return repr, used_hints, total_time

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("algo", type=int, help="Which algo to use", choices=(1,2))
    parser.add_argument("N", type=int, help="Size for NxN Box grid")
    parser.add_argument("H", type=int, help="The starting value for allowed_hints")
    parser.add_argument("T", type=int, help="Number of tries before allowed_hints += 1")
    args = parser.parse_args()

    if args.algo == 1:
        print(final(args.N, True, args.H, args.T, True))
    elif args.algo == 2:
        print(final(args.N, False, args.H, args.T, True))
