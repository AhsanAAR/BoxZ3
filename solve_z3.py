import z3 as z
# core and satisfying subsetes z3 microsoft.xs

with open('input.txt', 'r') as file:
    N = int(file.readline())

    row_vals = list(map(int, file.readline().split(',')))
    col_vals = list(map(int, file.readline().split(',')))

    row_ans = list(map(int, file.readline().split(',')))
    col_ans = list(map(int, file.readline().split(',')))

grid = [
    [z.Bool(f"x_{r}_{c}") for c in range(N)]
    for r in range(N)
]

row_vars = [
    [z.Int(f"r_{r}_{c}") for c in range(N)]
    for r in range(N)
]

col_vars = [
    [z.Int(f"c_{r}_{c}") for c in range(N)]
    for r in range(N)
]

solver = z.Solver()

for r in range(N):
    for c in range(N):
        solver.add(z.Implies(grid[r][c], z.And(row_vars[r][c] == col_vals[c], col_vars[r][c] == row_vals[r])))
        solver.add(z.Implies(z.Not(grid[r][c]), z.And(row_vars[r][c] == 0, col_vars[r][c] == 0)))

for r in range(N):
    solver.add(sum(row_vars[r]) == row_ans[r])

for c in range(N):
    col_list = []
    for r in range(N):
        col_list.append(col_vars[r][c])
    
    solver.add(sum(col_list) == col_ans[c])

if solver.check() == z.sat:
    model = solver.model()

    answer = [
        [model[grid[r][c]] for c in range(N)]
        for r in range(N)
    ]

    print(answer)

    with open('z3_out.txt', 'w') as file:
        for r in answer:
            file.write(f'{",".join(map(lambda x: "1" if x else "0", r))}\n')

else:
    print("Not possible")
