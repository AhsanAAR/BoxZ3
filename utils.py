import z3 as z

def first_n_primes(n):
    primes = []
    num = 2

    while len(primes) < n:
        is_prime = True
        for p in primes:
            if p * p > num:
                break
            if num % p == 0:
                is_prime = False
                break

        if is_prime:
            primes.append(num)
        num += 1

    return primes

def can_sum(arr: list[int], remove:int, target: int):
    if remove in arr:
        arr.remove(remove)
    else:
        return True
    
    s = z.Solver()
    vars = [z.Int(f"check_{i}") for i in range(len(arr))]
    for i in range(len(arr)):
        s.add(z.Or(vars[i] == 0, vars[i] == arr[i]))
    
    s.add(sum(vars) == target)
    arr.append(remove)

    return s.check() == z.sat

def reset_human_input():
    with open('input.txt', 'r') as file:
        N = int(file.readline())
    
    with open('human_input.txt', 'w') as file:
        for _ in range(N):
            file.write(",".join('0' for _ in range(N)) + "\n")

def save_file(id, to="input.txt", mode='a'):
    with open(to, "r") as src, open(f"saved_{id}.txt", mode) as dest:
        dest.write(src.read())

def grid_to_binary(grid):
    return "".join(str(val) for row in grid for val in row)

def cube_to_binary(cube):
    return "".join(str(val) for face in cube for row in face for val in row)