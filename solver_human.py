import z3 as z

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

def solver(msgs=False):
    while True:

        with open('human_aux.txt', 'r') as file:
            N = int(file.readline())

            row_vals = list(map(int, file.readline().split(',')))
            col_vals = list(map(int, file.readline().split(',')))

            row_ans = list(map(int, file.readline().split(',')))
            col_ans = list(map(int, file.readline().split(',')))

            current_grid = []
            for r in range(N):
                current_grid.append(list(map(int, file.readline().split(','))))

        row_decided_sum = []
        row_undecided_sum = []
        row_smallest_undecided = []
        row_undecided = []

        for r in range(N):
            dec = []
            un_dec = []

            for c in range(N):
                if current_grid[r][c] == 1:
                    dec.append(col_vals[c])
                elif current_grid[r][c] == 0:
                    un_dec.append(col_vals[c])
            
            row_decided_sum.append(sum(dec))
            row_undecided_sum.append(sum(un_dec))
            row_smallest_undecided.append(min(un_dec) if un_dec else 0)
            row_undecided.append(un_dec)


        col_decided_sum = []
        col_undecided_sum = []
        col_smallest_undecided = []
        col_undecided = []

        for c in range(N):
            dec = []
            un_dec = []

            for r in range(N):
                if current_grid[r][c] == 1:
                    dec.append(row_vals[r])
                elif current_grid[r][c] == 0:
                    un_dec.append(row_vals[r])

            col_decided_sum.append(sum(dec))
            col_undecided_sum.append(sum(un_dec))
            col_smallest_undecided.append(min(un_dec) if un_dec else 0)
            col_undecided.append(un_dec)

        grid = [
            [z.Int(f"x_{r}_{c}") for c in range(N)]
            for r in range(N)
        ]

        solver = z.Solver()

        for r in range(N):
            for c in range(N):
                solver.add(z.And(grid[r][c] >= -1, grid[r][c] <= 1))
                solver.add(z.Implies(current_grid[r][c] != 0, current_grid[r][c] == grid[r][c]))

        # rule 1


        for r in range(N):
            for c in range(N):
                # 1) range of values, carry-forward previous state
                solver.add(z.And(grid[r][c] >= -1, grid[r][c] <= 1))
                solver.add(z.Implies(current_grid[r][c] != 0, current_grid[r][c] == grid[r][c]))

                # 2) Mark cell unshaded whose row/column value is more than the remaning required sum
                solver.add(z.Implies(z.And(current_grid[r][c] == 0,row_ans[r] - row_decided_sum[r] < col_vals[c]), grid[r][c] == -1))
                solver.add(z.Implies(z.And(current_grid[r][c] == 0,col_ans[c] - col_decided_sum[c] < row_vals[r]), grid[r][c] == -1))

                # 3) If the sum of the undecided cells apart from this cell is smaller than the required target, shade it.
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, row_undecided_sum[r] - col_vals[c] < row_ans[r] - row_decided_sum[r]), grid[r][c] == 1))
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, col_undecided_sum[c] - row_vals[r] < col_ans[c] - col_decided_sum[c]), grid[r][c] == 1))

                # 4) If target - cell < smallest undecided cell, then make this cell unshaded.
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, row_ans[r] - row_decided_sum[r]-col_vals[c] < row_smallest_undecided[r], row_ans[r] - row_decided_sum[r]-col_vals[c] > 0), grid[r][c] == -1))
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, col_ans[c] - col_decided_sum[c]-row_vals[r] < col_smallest_undecided[c], col_ans[c] - col_decided_sum[c]-row_vals[r] > 0), grid[r][c] == -1))
                
                # 5) If the undecided cells apart from this one cannot create a sum equal to target, shade this cell. This covers some other rules, but is costly.
                r_cs = can_sum(row_undecided[r], col_vals[c], row_ans[r]-row_decided_sum[r])
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, z.Not(r_cs)), grid[r][c] == 1))

                c_cs = can_sum(col_undecided[c], row_vals[r], col_ans[c]-col_decided_sum[c])
                solver.add(z.Implies(z.And(current_grid[r][c] == 0, z.Not(c_cs)), grid[r][c] == 1))

        if solver.check() == z.sat:
            if msgs:
                print("made a step!")

            m = solver.model()

            answer = []

            for r in range(N):
                acc = []
                for c in range(N):
                    v = m[grid[r][c]]
                    solver.push()

                    solver.append(grid[r][c] == v * -1)
                    if solver.check() == z.sat:
                        acc.append(0)
                    else:
                        acc.append(v)
                    solver.pop()

                answer.append(acc)

            if answer == current_grid:
                if msgs:
                    print("reached equilibrium")
                return 0

            with open('human_aux.txt', 'w') as file:
                file.write(f"{N}\n")
                file.write(f"{','.join(map(str,row_vals))}\n")
                file.write(f"{','.join(map(str,col_vals))}\n")
                file.write(f"{','.join(map(str,row_ans))}\n")
                file.write(f"{','.join(map(str,col_ans))}\n")

                for r in answer:
                    file.write(f"{','.join(map(str,r))}\n")

                if 0 not in [answer[r][c] for c in range(N) for r in range(N)]:
                    if msgs:
                        print("Reached an answer!")

                    with open('input.txt', 'r') as ansfile:
                        ansfile.readline()
                        ansfile.readline()
                        ansfile.readline()
                        ansfile.readline()
                        ansfile.readline()

                        ground_truth = []
                        for r in range(N):
                            ground_truth.append(list(map(int, ansfile.readline().split(',')))) 

                    if ground_truth == answer:
                        if msgs:
                            print('Correct Answer!')
                        return 1
                    else:
                        if msgs:
                            print('Incorrect Answer!')
                        return -1
        else:
            if msgs:
                print("halt!")
            return -2 

if __name__ == "__main__":
    solver(True)
