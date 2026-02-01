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

def save_input(id, to="input.txt"):
    with open(to, "r") as src, open(f"saved_{id}.txt", "a") as dest:
        dest.write(src.read())

def grid_to_binary(grid):
    return "".join(str(val) for row in grid for val in row)

def cube_to_binary(cube):
    return "".join(str(val) for face in cube for row in face for val in row)