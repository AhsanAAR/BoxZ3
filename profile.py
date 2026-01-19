from generate_solvable import generate_solvable1, generate_solvable2
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("N", type=int, help="Size for NxN Box grid")

    args = parser.parse_args()

    N = args.N
    K = 10

    exclusion = set()
    total_unique_time = 0
    total_human_time = 0
    total_algo_1_time = 0
    total_algo_2_time = 0

    for k in range(K):
        print(k)
        repr1, unique_time, human_time, algo_1_time = generate_solvable1(N)
        repr2, algo_2_time = generate_solvable2(N)

        total_unique_time += unique_time
        total_human_time += human_time
        total_algo_1_time += algo_1_time
        total_algo_2_time += algo_2_time 

    print(N, K, total_unique_time/K, total_human_time/K, total_algo_1_time/K, total_algo_2_time/K)
