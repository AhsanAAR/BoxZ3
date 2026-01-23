from final import final
import argparse

if __name__ == "__main__":
    # parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    # parser.add_argument("N", type=int, help="Size for NxN Box grid")

    # args = parser.parse_args()

    K = 10

    for n in range(12, 30):
        total_time_unique = 0
        total_hints_unique = 0
        total_time_random = 0
        total_hints_random = 0

        hints_start = int(n*n*0.2)

        for k in range(K):
            print(k)
            # _, unique_hints, unique_time = final(n, True, hints_start=hints_start)
            _, random_hints, random_time = final(n, False, hints_start=hints_start)

            # total_time_unique += unique_time
            # total_hints_unique += unique_hints

            total_time_random += random_time
            total_hints_random += random_hints
        
        print(n, hints_start, total_time_unique/K, total_hints_unique/K, total_time_random/K, total_hints_random/K)
