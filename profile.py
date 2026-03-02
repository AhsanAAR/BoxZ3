from generate_solvable import generate_solvable1, generate_solvable2
import argparse

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    # parser.add_argument("N", type=int, help="Size for NxN Box grid")

    # args = parser.parse_args()

    K = 10

    for N in range(4, 11):
        total_algo_2_time = 0
        total_candidates_2 = 0

        for k in range(K):
            print(k)

            repr2, algo_2_time, candidates_2 = generate_solvable2(N)
            print(repr2, algo_2_time, candidates_2)
 
            total_algo_2_time += algo_2_time 
            total_candidates_2 += candidates_2

        print(N, K, total_algo_2_time/K, total_candidates_2/K)

    for N in range(4, 11):
        total_unique_time = 0
        total_human_time = 0
        total_algo_1_time = 0
        total_candidates_1 = 0
        total_unique_candidates = 0

        for k in range(K):
            print(k)

            repr1, unique_time, human_time, algo_1_time, unique_candidates, total_candidates = generate_solvable1(N)
            print(repr1, unique_time, human_time, algo_1_time, unique_candidates, total_candidates)
            
            total_unique_time += unique_time
            total_human_time += human_time
            total_algo_1_time += algo_1_time
            total_unique_candidates += unique_candidates
            total_candidates_1 += total_candidates
        
        print(N, K, total_unique_time/K, total_human_time/K, total_algo_1_time/K, total_unique_candidates/K, total_candidates_1/K)
