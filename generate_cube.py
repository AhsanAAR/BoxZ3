import random
import argparse
from utils import cube_to_binary, first_n_primes

def generate(N, exclusion=None):
    cube = [
        [
        [random.choice((1, 0)) for _ in range(N)]
        for _ in range(N)
        ]
        for _ in range(3)
    ]

    binary_repr = cube_to_binary(cube)

    if exclusion is not None:
        while binary_repr in exclusion:
            cube = [
                    [
                    [random.choice((1, 0)) for _ in range(N)]
                    for _ in range(N)
                    ]
                    for _ in range(3)
                ]
            binary_repr = cube_to_binary(cube)

    top_face = cube[0]
    left_face = cube[1]
    right_face = cube[2]

    # top_vals = [i+1 for i in range(N)]
    # right_vals = [i+1 for i in range(N)]
    # bottom_vals = [i+1 for i in range(N)]

    top_vals = first_n_primes(N)
    right_vals = first_n_primes(N)
    bottom_vals = first_n_primes(N)

    bottom_ans = [0 for _ in range(N)]

    for r in range(N):
        for c in range(N):
            bottom_ans[c] += top_face[r][c] * bottom_vals[N-1-r]
            bottom_ans[c] += left_face[r][c] * right_vals[r]

    left_ans = [0 for _ in range(N)]

    for r in range(N):
        for c in range(N):
            left_ans[r] += left_face[r][c] * top_vals[c]
            left_ans[r] += right_face[r][c] * bottom_vals[c]

    top_ans = [0 for _ in range(N)]

    for r in range(N):
        for c in range(N):
            top_ans[r] += top_face[r][c] * top_vals[c]
    
    for r in range(N):
        for c in range(N):
            top_ans[N-1-c] += right_face[r][c] * right_vals[r]

    with open('input_cube.txt', 'w') as file:
        file.write(f"{N}\n")
        file.write(f"{','.join(map(str,top_vals))}\n")
        file.write(f"{','.join(map(str,right_vals))}\n")
        file.write(f"{','.join(map(str,bottom_vals))}\n")

        file.write(f"{','.join(map(str,top_ans))}\n")
        file.write(f"{','.join(map(str,left_ans))}\n")
        file.write(f"{','.join(map(str,bottom_ans))}\n")

        for face in cube:
            for r in face:
              file.write(f"{','.join(map(lambda x: '1' if x else '-1',r))}\n")
    
    with open('human_input_cube.txt', 'w') as file:
        for face in cube:
            for _ in range(N):
                file.write(",".join('0' for _ in range(N)) + "\n")

    return binary_repr

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generates a random Cube BOX puzzle")
    parser.add_argument("N", type=int, help="Size for NxNxN Box Cube")
    args = parser.parse_args()

    generate(args.N)