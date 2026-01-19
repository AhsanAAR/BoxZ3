import random
import argparse
from utils import grid_to_binary

def generate(N, exclusion=None):
    grid = [
        [random.choice((1, 0)) for _ in range(N)]
        for _ in range(N)
    ]
    binary_repr = grid_to_binary(grid)

    if exclusion is not None:
        while binary_repr in exclusion:
            grid = [
                [random.choice((1, 0)) for _ in range(N)]
                for _ in range(N)
            ]
            binary_repr = grid_to_binary(grid)

    row_vals = [i+1 for i in range(N)]
    col_vals = [i+1 for i in range(N)]

    row_ans = []
    for r in range(N):
        acc = 0

        for c in range(N):
            if grid[r][c]:
                acc += col_vals[c]
        
        row_ans.append(acc)

    col_ans = []
    for c in range(N):
        acc = 0

        for r in range(N):
            if grid[r][c]:
                acc += row_vals[r]
        
        col_ans.append(acc)

    with open('input.txt', 'w') as file:
        file.write(f"{N}\n")
        file.write(f"{','.join(map(str,row_vals))}\n")
        file.write(f"{','.join(map(str,col_vals))}\n")
        file.write(f"{','.join(map(str,row_ans))}\n")
        file.write(f"{','.join(map(str,col_ans))}\n")

        for r in grid:
            file.write(f"{','.join(map(lambda x: '1' if x else '-1',r))}\n")

    return binary_repr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Box puzzle")
    parser.add_argument("N", type=int, help="Size for NxN Box grid")
    args = parser.parse_args()

    generate(args.N)