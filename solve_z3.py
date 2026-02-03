import z3 as z
# core and satisfying subsetes z3 microsoft.xs

def all_smt(s, initial_terms):
    def block_term(s, m, t):
        s.add(t != m.eval(t, model_completion=True))
    def fix_term(s, m, t):
        s.add(t == m.eval(t, model_completion=True))
    def all_smt_rec(terms):
        if z.sat == s.check():
           m = s.model()
           yield m
           for i in range(len(terms)):
               s.push()
               block_term(s, m, terms[i])
               for j in range(i):
                   fix_term(s, m, terms[j])
               yield from all_smt_rec(terms[i:])
               s.pop()   
    yield from all_smt_rec(list(initial_terms))

def solve_z3(write_ans=False, list_all=False):
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

    i = 0
    if solver.check() == z.sat:
        if write_ans:
            open("z3_out.txt", "w").close()

        
        for model in all_smt(solver, [grid[r][c] for c in range(N) for r in range(N)]):
            i+=1

            if write_ans:
                answer = [
                    [model[grid[r][c]] for c in range(N)]
                    for r in range(N)
                ]

                with open('z3_out.txt', 'a') as file:
                    for r in answer:
                        file.write(f'{",".join(map(lambda x: "1" if x else "0", r))}\n')
            
            if i == 2 and not list_all:
                return 2
            
    else:
        print("Not possible")
    
    return i

if __name__ == "__main__":
    print(solve_z3(False, True))
