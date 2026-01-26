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
    with open('input_cube.txt', 'r') as file:
        N = int(file.readline())

        top_vals = list(map(int, file.readline().split(',')))
        right_vals = list(map(int, file.readline().split(',')))
        bottom_vals = list(map(int, file.readline().split(',')))

        top_ans = list(map(int, file.readline().split(',')))
        left_ans = list(map(int, file.readline().split(',')))
        bottom_ans = list(map(int, file.readline().split(',')))

    top_face = [
        [z.Bool(f"t_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    left_face = [
        [z.Bool(f"l_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    right_face = [
        [z.Bool(f"r_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]

    top_row_vars = [
        [z.Int(f"tr_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    top_col_vars = [
        [z.Int(f"tc_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]

    left_row_vars = [
        [z.Int(f"lr_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    left_col_vars = [
        [z.Int(f"lc_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]

    right_row_vars = [
        [z.Int(f"rr_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]
    right_col_vars = [
        [z.Int(f"rc_{r}_{c}") for c in range(N)]
        for r in range(N)
    ]

    solver = z.Solver()

    for r in range(N):
        for c in range(N):
            solver.add(z.Implies(top_face[r][c], z.And(top_row_vars[r][c] == top_vals[c], top_col_vars[r][c] == bottom_vals[N-1-r])))
            solver.add(z.Implies(left_face[r][c], z.And(left_row_vars[r][c] == top_vals[c], left_col_vars[r][c] == right_vals[r])))
            solver.add(z.Implies(right_face[r][c], z.And(right_row_vars[r][c] == bottom_vals[c], right_col_vars[r][c] == right_vals[r])))
          
            solver.add(z.Implies(z.Not(top_face[r][c]), z.And(top_row_vars[r][c] == 0, top_col_vars[r][c] == 0)))
            solver.add(z.Implies(z.Not(left_face[r][c]), z.And(left_row_vars[r][c] == 0, left_col_vars[r][c] == 0)))
            solver.add(z.Implies(z.Not(right_face[r][c]), z.And(right_row_vars[r][c] == 0, right_col_vars[r][c] == 0)))
          
    

    for i in range(N):
        solver.add(top_ans[i] == (sum(top_row_vars[i]) + sum(right_col_vars[r][N-1-i] for r in range(N))))

        solver.add(left_ans[i] == (sum(left_row_vars[i]) + sum(right_row_vars[i])))

        solver.add(bottom_ans[i] == (sum(left_col_vars[r][i] for r in range(N)) + sum(top_col_vars[r][i] for r in range(N))))


    i = 0
    if solver.check() == z.sat:
        if write_ans:
            open("z3_out_cube.txt", "w").close()

        VARS = [top_face[r][c] for c in range(N) for r in range(N)] + [left_face[r][c] for c in range(N) for r in range(N)] + [right_face[r][c] for c in range(N) for r in range(N)]
        
        for model in all_smt(solver, VARS):
            i+=1

            if i > 1 and not list_all:
                return i

            if write_ans:
                top_solution = [
                    [model[top_face[r][c]] for c in range(N)]
                    for r in range(N)
                ]

                left_solution = [
                    [model[left_face[r][c]] for c in range(N)]
                    for r in range(N)
                ]

                right_solution = [
                    [model[right_face[r][c]] for c in range(N)]
                    for r in range(N)
                ]

                with open('z3_out_cube.txt', 'a') as file:
                    for r in top_solution:
                        file.write(f'{",".join(map(lambda x: "1" if x else "0", r))}\n')

                    for r in left_solution:
                        file.write(f'{",".join(map(lambda x: "1" if x else "0", r))}\n')

                    for r in right_solution:
                        file.write(f'{",".join(map(lambda x: "1" if x else "0", r))}\n')

    else:
        print("Not possible")
    
    return i

if __name__ == "__main__":
    print(solve_z3(True, True))
