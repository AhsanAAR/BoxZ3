from final2 import final
import argparse
import math

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    # parser.add_argument("N", type=int, help="Size for NxN Box grid")

    # args = parser.parse_args()

    K = 10

    for n in range(4,16):
        total_time = 0
        total_hints = 0
        total_iterations = 0

        for k in range(K):
            print(k)

            repr, hints, time, iterations = final(n)
            print(repr, hints, time, iterations)


            total_time += time
            total_hints += hints
            total_iterations += iterations

        print(n, K, total_time/K, total_hints/K, total_iterations/K)

    # for n in range(4,16):
    #     total_time = 0
    #     total_hints = 0
    #     total_candidates = 0

    #     hints_start = max(0,int(((10.9*n - 100.9)*0.7)))

    #     for k in range(K):
    #         print(k)

    #         repr, hints, time, candidates = final(n, False, hints_start=hints_start)
    #         print(repr, hints, time, candidates)

    #         total_time += time
    #         total_hints += hints
    #         total_candidates += candidates
        
    #     print(n, K, hints_start, total_time/K, total_hints/K, total_candidates/K)
    

    # for n in range(4,11):
    #     total_time = 0
    #     total_hints = 0
    #     total_candidates = 0

    #     for k in range(K):
    #         print(k)

    #         repr, hints, time, candidates = final(n, True)
    #         print(repr, hints, time, candidates)

    #         total_time += time
    #         total_hints += hints
    #         total_candidates += candidates
        
    #     print(n, K, total_time/K, total_hints/K, total_candidates/K)
    
    