import z3 as z
from utils import can_sum

def solver_helper(msgs):
    def add_constraints(solver: z.Solver, current_ans, z3_ans, decided_sum, undecided_sum, smallest_undecided, undecided, ans, vals):
        
        # print("current_ans", current_ans)
        # print("z3_ans", z3_ans)
        # print("decided_sum", decided_sum)
        # print("undecided_sum", undecided_sum)
        # print("smallest_undecided", smallest_undecided)
        # print("undecided", undecided)
        # print("ans", ans)
        # print("vals", vals)
        # print("\n\n")

        for r in range(len(current_ans)):
            for c in range(len(current_ans[r])):
                # 2) Mark cell unshaded whose row/column value is more than the remaning required sum
                solver.add(z.Implies(z.And(current_ans[r][c] == 0,ans[r] - decided_sum[r] < vals[c]), z3_ans[r][c] == -1))

                # 3) If the sum of the undecided cells apart from this cell is smaller than the required target, shade it.
                solver.add(z.Implies(z.And(current_ans[r][c] == 0, undecided_sum[r] - vals[c] < ans[r] - decided_sum[r]), z3_ans[r][c] == 1))

                # 4) If target - cell < smallest undecided cell, then make this cell unshaded.
                solver.add(z.Implies(z.And(current_ans[r][c] == 0, ans[r] - decided_sum[r]-vals[c] < smallest_undecided[r], ans[r] - decided_sum[r]-vals[c] > 0), z3_ans[r][c] == -1))
                
                # 5) If the undecided cells apart from this one cannot create a sum equal to target, shade this cell. This covers some other rules, but is costly.
                r_cs = can_sum(undecided[r], vals[c], ans[r]-decided_sum[r])
                solver.add(z.Implies(z.And(current_ans[r][c] == 0, z.Not(r_cs)), z3_ans[r][c] == 1))

    with open('input_cube.txt', 'r') as file:
        N = int(file.readline())

        top_vals = list(map(int, file.readline().split(',')))
        right_vals = list(map(int, file.readline().split(',')))
        bottom_vals = list(map(int, file.readline().split(',')))

        top_ans = list(map(int, file.readline().split(',')))
        left_ans = list(map(int, file.readline().split(',')))
        bottom_ans = list(map(int, file.readline().split(',')))

    with open('human_input_cube.txt', 'r') as file:
        current_top = []
        for r in range(N):
            current_top.append(list(map(int, file.readline().split(',')))) 

        current_left = []
        for r in range(N):
            current_left.append(list(map(int, file.readline().split(',')))) 

        current_right = []
        for r in range(N):
            current_right.append(list(map(int, file.readline().split(',')))) 

    while True:
        current_cube = [current_top,current_left,current_right]
        z3_top = [
            [z.Int(f"t_{r}_{c}") for c in range(N)]
            for r in range(N)
        ]

        z3_left = [
            [z.Int(f"l_{r}_{c}") for c in range(N)]
            for r in range(N)
        ]

        z3_right = [
            [z.Int(f"r_{r}_{c}") for c in range(N)]
            for r in range(N)
        ]

        z3_cube = [z3_top,z3_left,z3_right]

        solver = z.Solver()

        for r in range(N):
            for c in range(N):
                solver.add(z.And(z3_top[r][c] >= -1, z3_top[r][c] <= 1))
                solver.add(z.Implies(current_top[r][c] != 0, current_top[r][c] == z3_top[r][c]))

                solver.add(z.And(z3_left[r][c] >= -1, z3_left[r][c] <= 1))
                solver.add(z.Implies(current_left[r][c] != 0, current_left[r][c] == z3_left[r][c]))

                solver.add(z.And(z3_right[r][c] >= -1, z3_right[r][c] <= 1))
                solver.add(z.Implies(current_right[r][c] != 0, current_right[r][c] == z3_right[r][c]))

        top_decided_sum = []
        top_undecided_sum = []
        top_smallest_undecided = []
        top_undecided = []
        current_ans = []
        z3_ans = []

        for i in range(N):
            dec = []
            un_dec = []
            ans_acc = []
            z3_acc = []

            for c in range(N):
                ans_acc.append(current_top[i][c])
                z3_acc.append(z3_top[i][c])

                if current_top[i][c] == 1:
                    dec.append(top_vals[c])
                elif current_top[i][c] == 0:
                    un_dec.append(top_vals[c])
            
            for r in range(N):
                ans_acc.append(current_right[r][N-1-i])
                z3_acc.append(z3_right[r][N-1-i])

                if current_right[r][N-1-i] == 1:
                    dec.append(right_vals[r])
                elif current_right[r][N-1-i] == 0:
                    un_dec.append(right_vals[r])

            top_decided_sum.append(sum(dec))
            top_undecided_sum.append(sum(un_dec))
            top_smallest_undecided.append(min(un_dec) if un_dec else 0)
            top_undecided.append(un_dec)
            current_ans.append(ans_acc)
            z3_ans.append(z3_acc)
        
        add_constraints(solver, current_ans, z3_ans, top_decided_sum, top_undecided_sum, top_smallest_undecided, top_undecided, top_ans, top_vals+right_vals)

        left_decided_sum = []
        left_undecided_sum = []
        left_smallest_undecided = []
        left_undecided = []
        current_ans = []
        z3_ans = []

        for i in range(N):
            dec = []
            un_dec = []
            ans_acc = []
            z3_acc = []

            for c in range(N):
                ans_acc.append(current_left[i][c])
                z3_acc.append(z3_left[i][c])

                if current_left[i][c] == 1:
                    dec.append(top_vals[c])
                elif current_left[i][c] == 0:
                    un_dec.append(top_vals[c])
            
            for c in range(N):
                ans_acc.append(current_right[i][c])
                z3_acc.append(z3_right[i][c])

                if current_right[i][c] == 1:
                    dec.append(bottom_vals[c])
                elif current_right[i][c] == 0:
                    un_dec.append(bottom_vals[c])

            left_decided_sum.append(sum(dec))
            left_undecided_sum.append(sum(un_dec))
            left_smallest_undecided.append(min(un_dec) if un_dec else 0)
            left_undecided.append(un_dec)
            current_ans.append(ans_acc)
            z3_ans.append(z3_acc)

        add_constraints(solver, current_ans, z3_ans, left_decided_sum, left_undecided_sum, left_smallest_undecided, left_undecided, left_ans, top_vals+bottom_vals)

        bottom_decided_sum = []
        bottom_undecided_sum = []
        bottom_smallest_undecided = []
        bottom_undecided = []
        current_ans = []
        z3_ans = []

        for i in range(N):
            dec = []
            un_dec = []
            ans_acc = []
            z3_acc = []

            for r in range(N-1,-1,-1):
                ans_acc.append(current_left[r][i])
                z3_acc.append(z3_left[r][i])

                if current_left[r][i] == 1:
                    dec.append(right_vals[r])
                elif current_left[r][i] == 0:
                    un_dec.append(right_vals[r])
            
            for r in range(N-1,-1,-1):
                ans_acc.append(current_top[r][i])
                z3_acc.append(z3_top[r][i])

                if current_top[r][i] == 1:
                    dec.append(bottom_vals[N-1-r])
                elif current_top[r][i] == 0:
                    un_dec.append(bottom_vals[N-1-r])

            bottom_decided_sum.append(sum(dec))
            bottom_undecided_sum.append(sum(un_dec))
            bottom_smallest_undecided.append(min(un_dec) if un_dec else 0)
            bottom_undecided.append(un_dec)
            current_ans.append(ans_acc)
            z3_ans.append(z3_acc)

        add_constraints(solver, current_ans, z3_ans, bottom_decided_sum, bottom_undecided_sum, bottom_smallest_undecided, bottom_undecided, bottom_ans, list(reversed(right_vals))+bottom_vals)

        if solver.check() == z.sat:
            if msgs:
                print("made a step!")

            m = solver.model()

            answer = []

            for i in range(3):
                acc_grid = []

                for r in range(N):
                    acc = []
                    for c in range(N):
                        v = m[z3_cube[i][r][c]]
                        solver.push()

                        solver.append(z3_cube[i][r][c] == v * -1)
                        if solver.check() == z.sat:
                            acc.append(0)
                        else:
                            acc.append(v)
                        solver.pop()

                    acc_grid.append(acc)
                
                answer.append(acc_grid)

            if answer == current_cube:
                if msgs:
                    print("reached equilibrium")
                return 0, answer

            if 0 not in [answer[i][r][c] for c in range(N) for r in range(N) for i in range(3)]:
                if msgs:
                    print("Reached an answer!")
                if msgs:
                    print('Correct Answer!')
                return 1, answer
            
        else:
            if msgs:
                print("halt!")
            return -2, answer
        
        current_top = answer[0]
        current_left = answer[1]
        current_right = answer[2]

def solver(msgs=False, write_ans=False):
    ans, cube = solver_helper(msgs)

    if write_ans:
        with open('human_output_cube.txt', 'w') as file:
            for face in cube:
                for r in face:
                    file.write(f"{','.join(map(str,r))}\n")
    
    return ans

if __name__ == "__main__":
    solver(True, True)
